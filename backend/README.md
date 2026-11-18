# MealMitra Backend (Python Django + DRF)

This is the active backend for MealMitra. It is built with **Python 3.13**, **Django 6.1**, **Django REST Framework (DRF)**, **SimpleJWT**, and **SQLite 3 (Django ORM)**.

---

## 📁 Directory Structure & Code Map

```text
backend/
├── manage.py                  # Django CLI runner (runserver, migrate, seed_data, etc.)
├── requirements.txt           # Python dependencies
├── db.sqlite3                 # SQLite database file
├── .env.example               # Environment variables template
│
├── config/                    # Django Core Configuration
│   ├── settings.py            # Installed apps, SimpleJWT, CORS, database, middleware
│   ├── urls.py                # Root URL router connecting all apps and endpoints
│   ├── wsgi.py                # WSGI entry point
│   └── asgi.py                # ASGI entry point
│
├── apps/                      # Modular Business Applications
│   ├── accounts/              # 👤 User Authentication & Profiles
│   │   ├── models.py          # User (AbstractUser), UserProfile (1:1 Relationship)
│   │   ├── serializers.py     # UserSerializer, RegisterSerializer, CustomTokenObtainPair
│   │   ├── views.py           # Register, Login, Profile, Forgot/Reset Password
│   │   ├── urls.py            # /api/auth/*
│   │   ├── permissions.py     # IsAdminRole permission check
│   │   └── admin.py           # Django Admin User & UserProfile configuration
│   │
│   ├── plans/                 # 🍱 Tiffin Subscription Plans & Tags
│   │   ├── models.py          # TiffinPlan, Tag (Many-to-Many Relationship)
│   │   ├── serializers.py     # TiffinPlanSerializer, TagSerializer
│   │   ├── views.py           # PlanListCreateView, PlanDetailUpdateDeleteView, PlanAjaxSearchView
│   │   ├── urls.py            # /api/plans/*
│   │   ├── admin.py           # Admin management with tag filters
│   │   └── management/
│   │       └── commands/
│   │           └── seed_data.py # Seeds 18 initial meal plans, tags & test accounts
│   │
│   ├── orders/                # 📦 Customer Orders & Deliveries
│   │   ├── models.py          # Order (N:1 with User/Plan), Delivery (1:N with Order)
│   │   ├── serializers.py     # OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
│   │   ├── views.py           # Create order, user orders (/my), admin orders (/all), status update
│   │   ├── urls.py            # /api/orders/*
│   │   ├── admin.py           # Admin display with TabularInline deliveries
│   │   └── management/
│   │       └── commands/
│   │           └── clean_orders.py # Order consistency validator
│   │
│   ├── payments/              # 💳 Simulated Payment Processing (Lab Demo)
│   │   ├── views.py           # Create simulated Razorpay order, verify simulated payment
│   │   └── urls.py            # /api/payment/*
│   │
│   ├── chatbot/               # 💬 AI Meal Assistant (Local Database Engine)
│   │   ├── views.py           # Contextual recommendation engine querying SQLite
│   │   └── urls.py            # /api/chatbot/*
│   │
│   ├── reports/               # 📊 Reporting Services (College Syllabus Module 6)
│   │   ├── views.py           # ExportOrdersCSVView (csv module), ExportOrdersPDFView (ReportLab)
│   │   └── urls.py            # /api/reports/orders/csv/, /api/reports/orders/pdf/
│   │
│   ├── contact/               # ✉️ Inquiries & ModelForm Demonstration
│   │   ├── models.py          # ContactMessage model
│   │   ├── forms.py           # ContactForm (Django ModelForm with server validation)
│   │   ├── views.py           # ContactAPIView
│   │   └── urls.py            # /api/contact/*
│   │
│   └── lab_demo/              # 🎓 College Syllabus Demonstration App
│       ├── forms.py           # TiffinPlanModelForm
│       ├── views.py           # Function-based views for MVT, DTL, ModelForms, Relationships
│       └── urls.py            # /lab-demo/*
│
├── templates/                 # 📄 Django Templates (DTL)
│   ├── base.html              # Base layout with block inheritance (Module 3)
│   └── lab_demo/              # Demonstration templates:
│       ├── home.html          # Overview of Modules 1-6
│       ├── plans_list.html    # DTL loop, filters, QuerySet rendering
│       ├── plan_form.html     # ModelForm CSRF-protected form
│       ├── relationships.html # Visual inspection of 1:1, 1:N, N:M models
│       └── search.html        # Asynchronous AJAX live search
│
└── static/                    # 🎨 Static Assets for Django Demo
    ├── css/lab_demo.css       # Lab demo responsive styling
    └── js/lab_search.js       # Real-time AJAX search JavaScript
```

---

## ⚡ Useful Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server (port 8000)
python manage.py runserver 8000

# Run all automated tests
python manage.py test accounts plans orders payments chatbot reports lab_demo

# Apply database migrations
python manage.py migrate

# Seed initial 18 meal plans and accounts
python manage.py seed_data

# Create new migrations after editing models
python manage.py makemigrations
```
