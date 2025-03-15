import json
import logging
import uuid

from django.conf import settings
from django.urls import reverse
from django_daraja.mpesa.core import MpesaClient
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt  # change this during production use valid token
from .models import Order, Payment
from django.test import RequestFactory

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler for logging 
file_handler = logging.FileHandler('mpesa.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler for logging 
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger (note: addHandler is singular)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


@csrf_exempt 
def initiate_payment(request):
    logger.info('Initiate payment called')
    if request.method == 'POST':
        try:
            # Decode request body appropriately
            request_body = request.body.decode('utf-8') if isinstance(request.body, bytes) else request.body
            logger.debug(f'Raw request body: {request_body}')

            # Parse the request data depending on content type
            if request.content_type == 'application/json':
                data = json.loads(request_body)
            else:
                data = dict(request.POST)

            # Extract common fields
            phone_number = data.get('phone_number')
            amount = data.get('amount')
            order_id = data.get('order_id')
            full_name = data.get('full_name')
            email = data.get('email')
            country = data.get('country')
            state = data.get('state')
            payment_method = data.get('payment_method')

            # Generate order_id if missing
            if order_id is None:
                order_id = str(uuid.uuid4())
                logger.info(f'Generated unique order ID: {order_id}')

            if not amount:
                logger.warning('Amount is required')
                return JsonResponse({'error': 'Amount is required'}, status=400)

            try:
                amount = float(amount)
            except ValueError:
                logger.error('Invalid amount value')
                return JsonResponse({'error': 'Invalid amount value'}, status=400)

            logger.debug(f'Phone number: {phone_number}, Amount: {amount}, Order ID: {order_id}, '
                         f'Full Name: {full_name}, Email: {email}, Country: {country}, State: {state}, '
                         f'Payment Method: {payment_method}')

            # Initiate Mpesa payment
            cl = MpesaClient()
            account_reference = str(phone_number)
            transaction_desc = f'Payment for order {order_id}'
            ngrok_url = settings.ngrok_URL

            if ngrok_url:
                callback_url = f'{ngrok_url}/mpesa-callback/'
            else:
                callback_url = request.build_absolute_uri(reverse('mpesa-callback'))

            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            logger.info('Payment initiated successfully')
            response_data = response.json() if hasattr(response, 'json') else response

            if response_data is None or 'CheckoutRequestID' not in response_data:
                logger.error('Invalid response from M-Pesa API')
                return JsonResponse({'status': 'error', 'message': 'Invalid Response'})

            # Save payment info
            order = Order.objects.create(
                full_name=full_name,
                email=email,
                phone=phone_number,
                country=country,
                state=state,
                payment_method=payment_method,
                total_amount=amount
            )
            payment = Payment(
                order=order,
                method='mpesa',
                amount=amount,
                transaction_id=response_data.get('CheckoutRequestID', 'N/A')
            )
            payment.save()

            return JsonResponse({'status': 'success', 'response': response_data, 'order_id': order_id})
        except Exception as e:
            logger.error(f'Error initiating payment: {e}')
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        logger.warning('Invalid request method')
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def mpesa_callback(request):
    logger.info('Mpesa callback called')
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            response = json.loads(body)
            logger.debug(f'Callback response:{response}')

            if response['Body']['stkCallback']['ResultCode'] == 0:
                callback_metadata = response['Body']['stkCallback']['CallbackMetadata']
                merchant_request_id= response['Body']['stkCallback']['MerchantRequestID']
                checkout_request_id = response['Body']['stkCallback']['CheckoutRequestID']
                amount = next(item['Value'] for item in callback_metadata if item['Name'] == 'Amount')
                mpesa_receipt_number= next(item['Value'] for item in callback_metadata if item['Name'] == 'MpesaReceiptNumber')
                transaction_date= next(item['Value'] for item in callback_metadata if item['Name'] == 'TransactionDate')
                phone_number= next(item['Value'] for item in callback_metadata if item['Name'] == 'PhoneNumber')

                payment = Payment.objects.filter(transaction_id = checkout_request_id).first()
                if payment:
                    payment.status = 'completed'
                    payment.save()
                    order = payment.order
                    order.status = 'PAID'
                    order.save()
                    logger.info('Payment completed successfully')
                    return JsonResponse({'success':True})
                else:
                    logger.warning('Payment not found')
                    return JsonResponse({'success': False, 'message':'Payment not found'})
            else:
                logger.warning('Transaction Failed')
                return JsonResponse({'success':False,'message':'Transaction failed'})  

        except Exception as e:
            logger.error(f'Error in callback processing:{e}')
            return JsonResponse({'success':False,'message':str(e),status=500})
    else:
        logger.warning('Invalid request method')
        return JsonResponse({'succes':False,'message':'Invalid request method'})        


