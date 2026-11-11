# MealMitra Full Stack Project Migration Log
## Node.js / Express / MongoDB to Python Django / SQLite / Django ORM

This document serves as the master record of the full-stack migration of MealMitra. It tracks phase-by-phase execution, architectural changes, syllabus compliance, file modifications, and verification results.

---

## A. Project Overview

| Attribute | Original Project | Migrated Project |
|---|---|---|
| **Frontend** | React 19, Vite, Tailwind CSS, Axios, React Router v7 | React 19, Vite, Tailwind CSS, Axios, React Router v7 (Retained) |
| **Backend** | Node.js, Express.js 5 | Python 3.13, Django 6.1, Django REST Framework |
| **Database** | MongoDB Atlas, Mongoose 9 | SQLite 3, Django ORM |
| **Authentication** | Custom JWT (jsonwebtoken), bcryptjs | Django AbstractUser, Django REST Framework SimpleJWT, PBKDF2/Argon2 |
| **Administration** | Custom React Admin Dashboard | Django Admin + Custom React Admin Dashboard |
| **Payment** | Razorpay (checkout.js, HMAC verification) | Dummy simulated payment flow with mock confirmation |
| **Email** | Nodemailer (Gmail transport) | Simulated email notifications with console backend |
| **Chatbot / AI** | Google Gemini API (streamGenerateContent) | Simulated AI meal plan assistant with pre-configured contextual responses |
| **Streaming** | Server-Sent Events (SSE) | Frontend simulated typing effect (SSE replaced) |
| **Reporting** | None | Python CSV export + ReportLab PDF generator |
| **Syllabus Coverage**| Partial | Full coverage of Modules 1 to 6 (Full Stack Development Lab) |

### Migration Objectives
1. Migrate the backend completely to Python and Django.
2. Preserve the React 19 frontend UI, styling, user experience, and core functionality.
3. Replace MongoDB with SQLite and Django ORM implementing all core relationships (1:1, 1:N, N:M).
4. Safely convert payment, email, Gemini AI, and SSE streaming into robust dummy/mock implementations.
5. Provide a dedicated Django template inheritance and MVT demonstration section (`/lab-demo/`) for college lab evaluation.
6. Provide CSV and PDF report generation.
7. Maintain detailed change logs and Git history.

---

## B. Phase-wise Change Tracking

### Phase 1: Existing Project Analysis
- **Objective**: Comprehensively inspect the existing MERN stack codebase, understand models, routes, controllers, middleware, frontend components, and state management.
- **Work Completed**:
  - Analyzed all 29 backend files including Express routes, controllers, Mongoose models, and utilities.
  - Analyzed all 42 frontend files including components, pages, hooks, contexts, and services.
  - Mapped all 16 existing Express endpoints to their Django REST Framework equivalents.
  - Formulated the schema conversion plan from Mongoose to Django ORM.
  - Created migration plan artifact.
- **Files Modified/Created**:
  - Created artifact: `migration-plan.md`
  - Created git branch: `django-migration`
- **Tests Performed**:
  - Codebase inspection, route inventory verification, model schema mapping.
- **Git Commit Hash**: (Baseline branch creation)
- **Status**: Completed.

---

### Phase 2: Django Backend Setup
- **Objective**: Establish the Python Django environment, configure project structure, install dependencies, setup CORS, SQLite, SimpleJWT, and settings.
- **Work Completed**:
  - Created virtual environment and installed Django, DRF, SimpleJWT, django-cors-headers, python-decouple, and reportlab.
  - Scaffolded Django project `config` and modular apps: `accounts`, `plans`, `orders`, `payments`, `chatbot`, `reports`, `contact`, `lab_demo`.
  - Configured `settings.py` with custom user model, CORS middleware, REST framework JWT auth, and static/media/template paths.
  - Preserved original Node.js/Express backend by safely moving to `backend_legacy/` for full reference and verification.
  - Created `backend/.env.example` and updated `.gitignore` for Python artifacts.
- **Files Created / Modified**:
  - Added: `backend/manage.py`, `backend/requirements.txt`, `backend/.env.example`
  - Added: `backend/config/settings.py`, `backend/config/urls.py`, `backend/config/wsgi.py`, `backend/config/asgi.py`
  - Added apps: `backend/apps/accounts/`, `plans/`, `orders/`, `payments/`, `chatbot/`, `reports/`, `contact/`, `lab_demo/`
  - Modified: `.gitignore`
  - Preserved: `backend_legacy/`
- **Tests Performed**:
  - `python manage.py check` executed successfully (0 issues reported).
- **Git Commit Hash**: `c48ca51007ba8a2b3df57164ce2dd1bcd1154a58`
- **Status**: Completed.

---

### Phase 3: Database Migration
- **Objective**: Convert Mongoose schemas into Django models, implement model relationships (1:1, 1:N, N:M), execute database migrations, configure superuser, and seed initial data.
- **Work Completed**:
  - Implemented `accounts.User` extending `AbstractUser` and `accounts.UserProfile` (One-to-One relationship).
  - Implemented `plans.Tag` and `plans.TiffinPlan` with Many-to-Many tags relationship.
  - Implemented `orders.Order` with Many-to-One foreign keys to User and TiffinPlan.
  - Implemented `orders.Delivery` with One-to-Many foreign key to Order.
  - Implemented `contact.ContactMessage` for forms and validation demonstrations.
  - Generated and executed migrations for `accounts`, `plans`, `orders`, `contact`.
  - Built custom management command `python manage.py seed_data` and seeded all 18 original meal plans, 7 tags, default admin (`admin@mealmitra.com`), demo customer (`customer@mealmitra.com`), and sample orders.
- **Files Created / Modified**:
  - Added: `backend/apps/accounts/models.py`
  - Added: `backend/apps/plans/models.py`
  - Added: `backend/apps/orders/models.py`
  - Added: `backend/apps/contact/models.py`
  - Added: `backend/apps/plans/management/commands/seed_data.py`
  - Added: Initial migrations for accounts, plans, orders, contact
- **Tests Performed**:
  - `python manage.py makemigrations` and `python manage.py migrate` executed cleanly.
  - Seeding verified via Django shell: 2 Users, 18 Plans, 7 Tags, 2 Orders, 8 Deliveries.
- **Git Commit Hash**: (Pending Phase 3 commit)
- **Status**: Completed.

---

## C. Detailed File Change Register

| File / Directory | Action | Description | Reason |
|---|---|---|---|
| `.gitignore` | Modified | Added Python venv, pycache, and sqlite ignore rules | Prevent committing local environment artifacts |
| `backend_legacy/` | Renamed | Original Node.js / Express backend | Preserved intact for reference and rollback |
| `backend/requirements.txt` | Added | Python dependencies specification | Virtual environment dependency tracking |
| `backend/.env.example` | Added | Example environment variables for Django | Configuration template |
| `backend/manage.py` | Added | Django management script with apps path | Django CLI utility |
| `backend/config/settings.py` | Added | Django settings (CORS, JWT, DRF, apps, DB) | Core Django project configuration |
| `backend/config/urls.py` | Added | Main URL configuration | Routing root |
| `backend/config/wsgi.py` | Added | WSGI server entry point | Deployment compatibility |
| `backend/config/asgi.py` | Added | ASGI server entry point | Async compatibility |
| `backend/apps/accounts/models.py` | Added | Custom `User` model extending `AbstractUser` | Replaces MongoDB User schema |
| `backend/apps/*` | Added | Modular Django app skeletons | MVT and DRF modular design |

---

## D. Feature Migration Matrix

| Feature | Original Implementation | New Implementation | Status |
|---|---|---|---|
| User Registration | Express + bcrypt + Mongoose | Django REST Framework + Django Password Hashing | In Progress (Phase 3-4) |
| User Login | Express + jsonwebtoken | SimpleJWT (AccessToken & RefreshToken) | In Progress (Phase 3-4) |
| Profile Fetch | Express JWT middleware | DRF IsAuthenticated + UserSerializer | In Progress (Phase 3-4) |
| Forgot/Reset Password | Express + Nodemailer | Django Token Generator / Mocked email link | In Progress (Phase 4) |
| Meal Plans Catalog | Express + Mongoose find() | Django ORM QuerySet + PlanSerializer | In Progress (Phase 3-4) |
| Admin Plan CRUD | Express + isAdmin middleware | DRF ModelViewSet / IsAdminUser | In Progress (Phase 3-4) |
| Customer Order Placement | Express + Mongoose save() | Django ORM Transaction + OrderSerializer | In Progress (Phase 3-4) |
| Customer Orders List | Express + populate() | Django ORM select_related / prefetch_related | In Progress (Phase 3-4) |
| Admin Orders List & Update | Express + Socket.IO emit | Django ORM + DRF Views | In Progress (Phase 3-4) |
| Payment Integration | Razorpay Orders & Verification | Mock Payment Flow with instant simulated confirmation | Planned (Phase 6) |
| Email Notifications | Nodemailer with Gmail SMTP | Console Backend / Mock Responses | Planned (Phase 6) |
| AI Chatbot | Google Gemini API + SSE | Local Conversational Engine + Mock Typing | Planned (Phase 6) |
| CSV Order Export | None | Django `csv` module export endpoint | Planned (Phase 7) |
| PDF Order Reports | None | ReportLab PDF generator endpoint | Planned (Phase 7) |
| AJAX Search | None (Client-side only) | Server-side AJAX Search + Filter API | Planned (Phase 7) |
| Django Lab Demo (MVT) | None | Dedicated `/lab-demo/` DTL template inheritance app | Planned (Phase 7) |

---

## E. Dependency Change Register

### Python Dependencies Added
- `Django==6.1.3`: Core Python web framework.
- `djangorestframework==3.18.3`: REST API framework for Django.
- `djangorestframework_simplejwt==5.5.1`: JWT authentication for REST APIs.
- `django-cors-headers==4.9.0`: Handling Cross-Origin Resource Sharing with React.
- `python-decouple==3.8`: Safe environment variable loading.
- `reportlab==5.1.0`: PDF report generation for College Syllabus Module 6.
- `pillow==13.0.0`: Image processing support for ReportLab.

### Node Dependencies to be Sunsetted
- `mongoose`: Replaced by Django ORM.
- `express`: Replaced by Django / DRF.
- `jsonwebtoken`, `bcryptjs`: Replaced by Django auth & SimpleJWT.
- `razorpay`: Replaced by simulated payment flow.
- `nodemailer`: Replaced by Django console email.
- `socket.io`, `socket.io-client`: Real-time replaced with polling/direct REST.

---

## F. API Migration Register

| # | HTTP Method | Original Express Route | New Django Route | Auth Level | Migration Status |
|---|---|---|---|---|---|
| 1 | POST | `/api/auth/register` | `/api/auth/register/` | Public | Planned |
| 2 | POST | `/api/auth/login` | `/api/auth/login/` | Public | Planned |
| 3 | POST | `/api/auth/forgot-password` | `/api/auth/forgot-password/` | Public | Planned (Mocked) |
| 4 | POST | `/api/auth/reset-password/:token`| `/api/auth/reset-password/<token>/` | Public | Planned (Mocked) |
| 5 | GET | `/api/auth/profile` | `/api/auth/profile/` | Authenticated | Planned |
| 6 | POST | *(new)* | `/api/auth/token/refresh/` | Public | Planned |
| 7 | GET | `/api/plans` | `/api/plans/` | Public | Planned |
| 8 | POST | `/api/plans` | `/api/plans/` | Admin | Planned |
| 9 | PUT | `/api/plans/:id` | `/api/plans/<id>/` | Admin | Planned |
| 10 | DELETE | `/api/plans/:id` | `/api/plans/<id>/` | Admin | Planned |
| 11 | POST | `/api/orders` | `/api/orders/` | Authenticated | Planned |
| 12 | GET | `/api/orders/my` | `/api/orders/my/` | Authenticated | Planned |
| 13 | GET | `/api/orders/all` | `/api/orders/all/` | Admin | Planned |
| 14 | PUT | `/api/orders/:id` | `/api/orders/<id>/` | Admin | Planned |
| 15 | POST | `/api/payment/create-order` | `/api/payment/create-order/` | Authenticated | Planned (Mocked) |
| 16 | POST | `/api/payment/verify` | `/api/payment/verify/` | Authenticated | Planned (Mocked) |
| 17 | POST | `/api/chatbot` | `/api/chatbot/` | Public | Planned (Mocked) |
| 18 | GET | *(new)* | `/api/reports/orders/csv/` | Admin | Planned |
| 19 | GET | *(new)* | `/api/reports/orders/pdf/` | Admin | Planned |
| 20 | GET | *(new)* | `/api/plans/search/` | Public | Planned |

---

## G. Database Migration Register

| MongoDB Collection | Mongoose Schema | Django Model | Relationships | Status |
|---|---|---|---|---|
| `users` | `User` | `accounts.User` | 1:N with `orders.Order` | Schema Defined |
| `tiffinplans` | `TiffinPlan` | `plans.TiffinPlan` | 1:N with `orders.Order`, N:M with `plans.Tag` | Planned |
| `orders` | `Order` | `orders.Order` | N:1 with `User`, N:1 with `TiffinPlan`, 1:N with `Delivery` | Planned |
| `orders.deliveries` | Embedded Subdocument | `orders.Delivery` | N:1 with `orders.Order` | Planned |
| *(new)* | None | `plans.Tag` | N:M with `plans.TiffinPlan` | Planned |
| *(new)* | None | `contact.ContactMessage`| Standalone for Forms & CRUD demo | Planned |

---

## H. Syllabus Compliance Tracker

| Module | Topic | Implementation Target | File Location | Status |
|---|---|---|---|---|
| **Module 1** | Python & Django Fundamentals | Project setup, settings, apps | `backend/config/settings.py` | Implemented |
| **Module 1** | Virtual Environment | Isolated Python 3.13 venv | `backend/venv/` | Implemented |
| **Module 1** | MVT Architecture | Split apps, models, views, templates | `backend/apps/*` | In Progress |
| **Module 2** | Request-Response Cycle & URL Routing | Function-based views, URLconfs | `apps/lab_demo/views.py`, `urls.py` | Planned |
| **Module 2** | Django Templates & DTL | Context passing, filters, tags | `backend/templates/lab_demo/` | Planned |
| **Module 3** | Multi-page Development & Inheritance | `{% extends %}`, `{% block %}` | `backend/templates/base.html` | Planned |
| **Module 3** | Static Files & Responsive Layout | CSS, JS, static configuration | `backend/static/` | Planned |
| **Module 4** | Django ORM & Relationships | 1:1, 1:N, N:M models | `apps/*/models.py` | In Progress |
| **Module 4** | Django Forms & ModelForms | Server-side validation | `apps/contact/forms.py`, `apps/plans/forms.py` | Planned |
| **Module 4** | QuerySets, Filtering & Searching | Q objects, icontains, ordering | `apps/plans/views.py`, `apps/orders/views.py` | Planned |
| **Module 5** | Django Admin & Superuser | Custom ModelAdmin, search, filters | `apps/*/admin.py` | Planned |
| **Module 5** | Authentication & Authorization | Password hashing, permissions | `apps/accounts/` | In Progress |
| **Module 6** | CSV Export | Streaming/downloadable CSV | `apps/reports/views.py` | Planned |
| **Module 6** | PDF Report Generation | ReportLab dynamic PDF | `apps/reports/views.py` | Planned |
| **Module 6** | AJAX Integration & Real-time Search | Axios to Django API search | `apps/plans/views.py` + React UI | Planned |

---

## I. Known Issues and Pending Work

1. Complete Phase 3 (Database Models for plans, orders, tags, contact messages, and migrations).
2. Seed initial 18 meal plans into SQLite database.
3. Complete Phase 4 (REST API endpoints and serializers).
4. Integrate with React frontend (Phase 5).
5. Implement dummy payment and chatbot services (Phase 6).
6. Build Django lab demonstration section with template inheritance (Phase 7).

---

## J. Phase 2 Verification & Commit Details
- **Verification**: `python manage.py check` returned 0 issues.
- **Git Commit Hash**: [Pending next commit]
