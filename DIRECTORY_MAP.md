# MealMitra Directory Map & Code Index

This document is your quick reference guide to finding any file, model, endpoint, or component across the MealMitra codebase.

---

## 🧭 High-Level Overview

```text
MealMitra/
├── backend/            👈 ACTIVE DJANGO BACKEND (Python 3.13, DRF, SQLite, ORM)
├── frontend/           👈 ACTIVE REACT 19 FRONTEND (Vite, Tailwind CSS, Axios)
├── legacy_archive/     👈 ARCHIVED LEGACY NODE.JS CODE (Preserved reference only)
├── README.md           👈 Project quickstart and setup instructions
├── DIRECTORY_MAP.md    👈 THIS FILE: Comprehensive code finder
└── MIGRATION_LOG.md    👈 Detailed phase-by-phase migration audit trail
```

---

## 🔍 Feature-to-File Finder

### 1. User Authentication & Accounts
| Feature | Backend File | Frontend File |
|---|---|---|
| **User Model** | [`backend/apps/accounts/models.py`](backend/apps/accounts/models.py) (`User` extending `AbstractUser`) | — |
| **Profile (1:1 Relationship)** | [`backend/apps/accounts/models.py`](backend/apps/accounts/models.py) (`UserProfile`) | — |
| **JWT Serializers** | [`backend/apps/accounts/serializers.py`](backend/apps/accounts/serializers.py) | — |
| **Registration** | [`backend/apps/accounts/views.py`](backend/apps/accounts/views.py) (`RegisterView`) | [`frontend/src/pages/Signup.jsx`](frontend/src/pages/Signup.jsx) |
| **Login & JWT Generation** | [`backend/apps/accounts/views.py`](backend/apps/accounts/views.py) (`LoginView`) | [`frontend/src/pages/Login.jsx`](frontend/src/pages/Login.jsx) |
| **Password Reset** | [`backend/apps/accounts/views.py`](backend/apps/accounts/views.py) (`ForgotPasswordView`, `ResetPasswordView`) | [`frontend/src/pages/ForgotPassword.jsx`](frontend/src/pages/ForgotPassword.jsx), [`ResetPassword.jsx`](frontend/src/pages/ResetPassword.jsx) |
| **Route Guards** | [`backend/apps/accounts/permissions.py`](backend/apps/accounts/permissions.py) (`IsAdminRole`) | [`frontend/src/components/ProtectedRoute.jsx`](frontend/src/components/ProtectedRoute.jsx), [`AdminRoute.jsx`](frontend/src/components/AdminRoute.jsx) |

---

### 2. Tiffin Meal Plans & Categories
| Feature | Backend File | Frontend File |
|---|---|---|
| **Plan & Tag Models** | [`backend/apps/plans/models.py`](backend/apps/plans/models.py) (`TiffinPlan`, `Tag` **N:M**) | — |
| **Plan Serializers** | [`backend/apps/plans/serializers.py`](backend/apps/plans/serializers.py) | — |
| **Plan Catalog API** | [`backend/apps/plans/views.py`](backend/apps/plans/views.py) (`PlanListCreateView`) | [`frontend/src/pages/Plans.jsx`](frontend/src/pages/Plans.jsx) |
| **Admin Plan CRUD** | [`backend/apps/plans/views.py`](backend/apps/plans/views.py) (`PlanDetailUpdateDeleteView`) | [`frontend/src/pages/AdminDashboard.jsx`](frontend/src/pages/AdminDashboard.jsx) |
| **Real-time AJAX Search**| [`backend/apps/plans/views.py`](backend/apps/plans/views.py) (`PlanAjaxSearchView`) | [`backend/static/js/lab_search.js`](backend/static/js/lab_search.js) |
| **18 Initial Plans Seed**| [`backend/apps/plans/management/commands/seed_data.py`](backend/apps/plans/management/commands/seed_data.py) | — |

---

### 3. Customer Orders & Delivery Tracking
| Feature | Backend File | Frontend File |
|---|---|---|
| **Order & Delivery Models** | [`backend/apps/orders/models.py`](backend/apps/orders/models.py) (`Order` **N:1**, `Delivery` **1:N**) | — |
| **Order Serializers** | [`backend/apps/orders/serializers.py`](backend/apps/orders/serializers.py) | — |
| **Place Order** | [`backend/apps/orders/views.py`](backend/apps/orders/views.py) (`OrderCreateView`) | [`frontend/src/pages/Plans.jsx`](frontend/src/pages/Plans.jsx) |
| **Customer Orders List** | [`backend/apps/orders/views.py`](backend/apps/orders/views.py) (`MyOrdersView`) | [`frontend/src/pages/Dashboard.jsx`](frontend/src/pages/Dashboard.jsx) |
| **Admin Orders List & Status** | [`backend/apps/orders/views.py`](backend/apps/orders/views.py) (`AllOrdersView`, `OrderDetailUpdateView`) | [`frontend/src/pages/AdminDashboard.jsx`](frontend/src/pages/AdminDashboard.jsx) |
| **Visual Delivery Tracker**| — | [`frontend/src/components/OrderTracker.jsx`](frontend/src/components/OrderTracker.jsx) |
| **Clean Orders Tool** | [`backend/apps/orders/management/commands/clean_orders.py`](backend/apps/orders/management/commands/clean_orders.py) | — |

---

### 4. Payment & Checkout (Simulated Demonstration)
| Feature | Backend File | Frontend File |
|---|---|---|
| **Payment Order Creation** | [`backend/apps/payments/views.py`](backend/apps/payments/views.py) (`CreateOrderView`) | [`frontend/src/pages/CheckoutPage.jsx`](frontend/src/pages/CheckoutPage.jsx) |
| **Payment Verification** | [`backend/apps/payments/views.py`](backend/apps/payments/views.py) (`VerifyPaymentView`) | [`frontend/src/pages/CheckoutPage.jsx`](frontend/src/pages/CheckoutPage.jsx) |
| **Payment Success Screen** | — | [`frontend/src/pages/PaymentSuccess.jsx`](frontend/src/pages/PaymentSuccess.jsx) |

---

### 5. AI Chatbot Assistant (Local Engine)
| Feature | Backend File | Frontend File |
|---|---|---|
| **Contextual Plan Queries**| [`backend/apps/chatbot/views.py`](backend/apps/chatbot/views.py) (`ChatbotView`) | [`frontend/src/services/chatStream.js`](frontend/src/services/chatStream.js) |
| **Chat State & Preferences**| — | [`frontend/src/hooks/useChat.js`](frontend/src/hooks/useChat.js), [`frontend/src/utils/chatPreferences.js`](frontend/src/utils/chatPreferences.js) |
| **Chat Widget UI** | — | [`frontend/src/components/chat/ChatWidget.jsx`](frontend/src/components/chat/ChatWidget.jsx), [`MarkdownMessage.jsx`](frontend/src/components/chat/MarkdownMessage.jsx) |

---

### 6. Reports & Data Export (Module 6)
| Feature | Backend File | Frontend Integration |
|---|---|---|
| **CSV Export** | [`backend/apps/reports/views.py`](backend/apps/reports/views.py) (`ExportOrdersCSVView`) | "Export CSV" button in [`frontend/src/pages/AdminDashboard.jsx`](frontend/src/pages/AdminDashboard.jsx) |
| **ReportLab PDF Generator** | [`backend/apps/reports/views.py`](backend/apps/reports/views.py) (`ExportOrdersPDFView`) | "Export PDF" button in [`frontend/src/pages/AdminDashboard.jsx`](frontend/src/pages/AdminDashboard.jsx) |

---

### 7. Inquiries & ModelForms (Module 4)
| Feature | Backend File | Frontend File |
|---|---|---|
| **Contact Message Model** | [`backend/apps/contact/models.py`](backend/apps/contact/models.py) (`ContactMessage`) | — |
| **Server-Side ModelForm** | [`backend/apps/contact/forms.py`](backend/apps/contact/forms.py) (`ContactForm`) | — |
| **Submission API** | [`backend/apps/contact/views.py`](backend/apps/contact/views.py) (`ContactAPIView`) | Form in [`frontend/src/pages/Contact.jsx`](frontend/src/pages/Contact.jsx) |

---

### 8. College Syllabus Demonstration Section (`/lab-demo/`)
| Concept | View | Template File |
|---|---|---|
| **Base Template & Inheritance** | — | [`backend/templates/base.html`](backend/templates/base.html) |
| **Overview of Modules 1-6** | `lab_demo_home` in [`apps/lab_demo/views.py`](backend/apps/lab_demo/views.py) | [`backend/templates/lab_demo/home.html`](backend/templates/lab_demo/home.html) |
| **DTL Loop, Filters & QuerySet** | `lab_demo_plans` in [`apps/lab_demo/views.py`](backend/apps/lab_demo/views.py) | [`backend/templates/lab_demo/plans_list.html`](backend/templates/lab_demo/plans_list.html) |
| **ModelForm with CSRF** | `lab_demo_plan_create` in [`apps/lab_demo/views.py`](backend/apps/lab_demo/views.py) | [`backend/templates/lab_demo/plan_form.html`](backend/templates/lab_demo/plan_form.html) |
| **ORM Relationships Inspector** | `lab_demo_relationships` in [`apps/lab_demo/views.py`](backend/apps/lab_demo/views.py) | [`backend/templates/lab_demo/relationships.html`](backend/templates/lab_demo/relationships.html) |
| **Asynchronous AJAX Live Search**| `lab_demo_search` in [`apps/lab_demo/views.py`](backend/apps/lab_demo/views.py) | [`backend/templates/lab_demo/search.html`](backend/templates/lab_demo/search.html) |

---

## 🗄️ Database & Configuration Files
- **Database File**: [`backend/db.sqlite3`](backend/db.sqlite3) (SQLite database storing all users, plans, tags, orders, deliveries, and inquiries)
- **Django Settings**: [`backend/config/settings.py`](backend/config/settings.py)
- **Django URLs**: [`backend/config/urls.py`](backend/config/urls.py)
- **Vite Proxy Config**: [`frontend/vite.config.js`](frontend/vite.config.js)
- **Axios HTTP Client**: [`frontend/src/services/api.js`](frontend/src/services/api.js)
