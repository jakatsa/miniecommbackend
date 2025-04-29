# 🌐 **EcommBackend**

A robust backend for an e-commerce platform built using **Django** and **Django REST Framework**. This backend powers functionalities like product management, user authentication, and vendor operations, with plans to integrate a seamless payment system.

---

## 🚀 **Features**

### ✅ **Current Features**

-
- **Product Management**:
  - List and retrieve products.
  - Add new products (vendor-only).
  - Improved user experience with dynamic filtering.

### 🌟 **Planned Features**

**User Authentication**:

- User registration and login.
- **Payment System Integration**:
  - Payment gateways like Mpesa and PayPal.
- **Order Management**:
  - Cart functionality and checkout process.
- **Vendor Dashboard**:
  -product and order management.

---

## 🛠️ **Tech Stack**

### **Backend Frameworks**

- **Django**: High-level Python framework for rapid development.
- **Django REST Framework**: Create scalable RESTful APIs.

### **Dependencies**

- **Pillow**: Image processing.
- **Django Filter**: Simplified query filtering.
- **Django CORS Headers**: Manage cross-origin resource sharing (CORS).
- **Sqlparse**: SQL parsing.

---

## 📁 **Project Structure**

```plaintext
ecommbackend/
├── backend/             # Main project configuration
│   ├── settings.py      # Django settings
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI application
├── apps/
│   ├── products/        # Product management app
│   ├── users/           # User authentication and profiles
│   └── vendors/         # Vendor-specific functionality
├── media/               # Uploaded product images
├── static/              # Static files (CSS, JS, etc.)
├── env/                 # Virtual environment (excluded from repo)
├── manage.py            # Django project entry point
├── requirements.txt     # Dependencies list
└── README.md            # Project documentation
```

## 💾 ** Installation**

git clone [<repository-url>](https://github.com/jakatsa/miniecommbackend)

## Step 2: Navigate to the Project Directory

cd ecommbackend

## Step 3: Create a Virtual Environment

python -m venv env
source env/bin/activate # Linux/Mac
env\Scripts\activate # Windows

## Step 4: run requirements.txt

python3 manage.py migrate

## Step 5: Apply Migrations

python3 manage.py migrate

## Step 5: Start the Development Server

python3 manage.py runserver 8080

## 📝 Future Enhancements

Payment Integration:
Enable secure transactions using third-party gateways.(Mpesa & PayPal)

Order Management:
Implement cart and checkout workflows.
Vendor Analytics:
Insights and metrics for vendors.

```

```
