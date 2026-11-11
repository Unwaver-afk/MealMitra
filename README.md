# MealMitra — Full Stack Tiffin Subscription Application

MealMitra is a full-stack web application for managing healthy daily tiffin subscriptions. The project features a modern **React 19** frontend communicating via REST APIs with a robust **Python Django** backend powered by **Django REST Framework (DRF)**, **SQLite**, and the **Django ORM**.

This project also includes a dedicated **Django Lab Demonstration** section (`/lab-demo/`) specifically designed to satisfy the **Full Stack Development Lab** college syllabus (Modules 1 through 6).

---

## 1. Technology Stack

### Frontend (Preserved React Application)
- **Framework**: React 19 (Vite 8)
- **Routing**: React Router v7
- **Styling**: Tailwind CSS 3 with `@tailwindcss/typography`
- **HTTP Client**: Axios with Bearer JWT interceptors
- **Markdown & Code**: React Markdown & Remark GFM
- **Theme**: Light & Dark mode support

### Backend (Python & Django)
- **Language**: Python 3.13+
- **Framework**: Django 6.1 (MVT architecture)
- **REST APIs**: Django REST Framework (DRF) 3.18
- **Authentication**: DRF SimpleJWT (JSON Web Tokens)
- **Database**: SQLite 3 with Django ORM
- **Forms**: Django Forms and ModelForms with server-side validation
- **Reporting**: Python `csv` module and ReportLab for PDF generation
- **CORS**: `django-cors-headers`

---

## 2. Project Architecture

```text
MealMitra/
├── backend/                         # Python Django Backend
│   ├── config/                      # Project Configuration
│   │   ├── settings.py              # Installed apps, SimpleJWT, CORS, DB
│   │   ├── urls.py                  # Main URL router
│   │   ├── wsgi.py / asgi.py        # Gateway interfaces
│   ├── apps/                        # Modular Django Applications
│   │   ├── accounts/                # User model (AbstractUser), 1:1 UserProfile, JWT Auth
│   │   ├── plans/                   # TiffinPlan, Tag (N:M), Plan serializers & views
│   │   ├── orders/                  # Order (N:1), Delivery (1:N), Order management
│   │   ├── payments/                # Simulated payment flow (create & verify)
│   │   ├── chatbot/                 # Contextual meal assistant querying SQLite
│   │   ├── reports/                 # CSV & PDF report generators (Module 6)
│   │   ├── contact/                 # Contact inquiries & Django ModelForm validation
│   │   └── lab_demo/                # DTL templates, template inheritance, AJAX search
│   ├── templates/                   # Django Templates (DTL)
│   │   ├── base.html                # Base layout template with inheritance blocks
│   │   └── lab_demo/                # Multi-page DTL views (home, plans, form, relationships, search)
│   ├── static/                      # Static assets for Django Lab Demo (CSS, JS)
│   ├── manage.py                    # Django CLI management script
│   └── requirements.txt             # Python dependencies
├── frontend/                        # React 19 Frontend
│   ├── src/                         # React components, pages, hooks, contexts
│   ├── public/                      # Static icons and meal images
│   ├── package.json                 # Node dependencies
│   └── vite.config.js               # Dev proxy configured to http://127.0.0.1:8000
├── backend_legacy/                  # Original Node.js/Express backend (Preserved reference)
├── MIGRATION_LOG.md                 # Master historical record of the complete migration
└── README.md
```

---

## 3. Getting Started & Installation

### Prerequisites
- **Python**: Version 3.11 or newer (Python 3.13 tested)
- **Node.js**: Version 20 or newer
- **npm**: Version 10 or newer

---

### Step 1: Set Up the Django Backend

1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # On macOS / Linux:
   python3 -m venv venv
   source venv/bin/activate

   # On Windows (PowerShell):
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations to SQLite:
   ```bash
   python manage.py migrate
   ```

5. Seed initial data (18 meal plans, tags, demo users, sample orders):
   ```bash
   python manage.py seed_data
   ```

6. Start the Django development server:
   ```bash
   python manage.py runserver 8000
   ```
   *The Django server runs at `http://127.0.0.1:8000/`.*

---

### Step 2: Set Up the React Frontend

1. Open a new terminal and navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The React application opens at `http://localhost:5173/`.*

---

## 4. Default Demonstration Credentials

The `seed_data` command automatically provisions default test accounts:

| Role | Email | Password | Access Privileges |
|---|---|---|---|
| **Administrator** | `admin@mealmitra.com` | `admin123456` | React Admin Dashboard, Django Admin (`/admin/`), Plan CRUD, Order status updates, CSV/PDF reports |
| **Customer** | `customer@mealmitra.com` | `user123456` | Customer Dashboard, browse plans, place subscriptions, simulated payments, live tracking |

---

## 5. College Lab Syllabus Compliance Mapping

This project maps directly to the **Full Stack Development Lab** syllabus modules:

| Syllabus Module | Key Topics Covered | Implementation in MealMitra | Key File Reference |
|---|---|---|---|
| **Module 1: Fundamentals** | Python programming, Django configuration, Virtual Environments, MVT, Settings | Modular application design, isolated virtual environment, Django settings, CORS headers | `backend/config/settings.py`<br>`backend/manage.py` |
| **Module 2: Views & Templates** | Request-Response Cycle, URL Routing, Function-based views, DTL, Context data | Function-based views passing QuerySets and statistics to DTL templates | `apps/lab_demo/views.py`<br>`templates/lab_demo/home.html` |
| **Module 3: Template Inheritance** | Multi-page development, `{% extends %}`, `{% block %}`, static CSS & JS, responsive layouts | Clean template inheritance tree from `base.html` with responsive emerald theme | `templates/base.html`<br>`static/css/lab_demo.css` |
| **Module 4: Django ORM & Forms** | 1:1, 1:N, N:M model relationships, CRUD operations, QuerySets, Django ModelForms, server validation | User ↔ Profile (1:1), User → Orders (1:N), Order → Delivery (1:N), Plan ↔ Tag (N:M), `TiffinPlanModelForm`, `ContactForm` | `apps/accounts/models.py`<br>`apps/plans/models.py`<br>`apps/orders/models.py`<br>`apps/lab_demo/forms.py` |
| **Module 5: Administration & Auth** | Django Admin customization, superuser, auth, password hashing, protected endpoints | Customized ModelAdmin with tabular inlines, list displays, filters, search, SimpleJWT | `apps/*/admin.py`<br>`apps/accounts/permissions.py`<br>`apps/accounts/serializers.py` |
| **Module 6: Reporting & AJAX** | CSV export, ReportLab PDF reports, AJAX search, interactive applications | Orders CSV streaming export, formatted PDF report generation, vanilla JS real-time AJAX search | `apps/reports/views.py`<br>`static/js/lab_search.js`<br>`apps/plans/views.py` |

---

## 6. Accessing Demonstration Portals

- **Main Customer App (React 19)**: [http://localhost:5173/](http://localhost:5173/)
- **React Admin Dashboard**: [http://localhost:5173/admin](http://localhost:5173/admin) *(Sign in as `admin@mealmitra.com`)*
- **Django Admin Portal**: [http://localhost:8000/admin/](http://localhost:8000/admin/) *(Sign in with admin credentials)*
- **Django Lab Demo Section**: [http://localhost:8000/lab-demo/](http://localhost:8000/lab-demo/) *(Multi-page MVT, DTL, ModelForms, and ORM Inspector)*
- **API Health Check**: [http://localhost:8000/health/](http://localhost:8000/health/)

---

## 7. Simulated Demonstration Features

To comply with lab and demonstration requirements without external third-party dependencies:
- **Simulated Payment Gateway**: When checking out, a simulated payment dialog processes test orders and updates the order to `Paid` in SQLite without contacting Razorpay servers.
- **Simulated AI Assistant**: The floating chatbot uses a local database query engine to recommend real plans matching customer queries (e.g., budget under ₹1000, vegetarian, breakfast, dinner) with simulated streaming typing.
- **Simulated Email Notifications**: Password resets and order receipts are logged safely to the console.

---

## 8. Running Automated Tests

Run backend tests across all applications:
```bash
cd backend
./venv/bin/python manage.py test accounts plans orders payments chatbot reports lab_demo
```
*Expected: 20 passed tests covering authentication, CRUD, permissions, reports, and templates.*

Run frontend production build verification:
```bash
cd frontend
npm run build
```
