# MealMitra Frontend (React 19 + Vite)

The customer-facing single-page application for MealMitra, built with **React 19**, **Vite 8**, **Tailwind CSS 3**, **React Router v7**, and **Axios**.

---

## 📁 Directory Structure & Code Map

```text
frontend/
├── vite.config.js             # Proxies /api and /lab-demo requests to Django (port 8000)
├── tailwind.config.js         # Theme and dark mode configuration
├── index.html                 # Single page application entry point
│
└── src/
    ├── main.jsx               # React DOM root mounting point
    ├── App.jsx                # Route definitions & top-level layout wrapper
    ├── index.css              # Tailwind base styles, typography & dark theme
    │
    ├── pages/                 # 🖥️ Screen Views (Connected to Routes)
    │   ├── Home.jsx           # Landing page with hero section & service categories
    │   ├── Plans.jsx          # Interactive subscription builder (Daily/Weekly/Monthly)
    │   ├── Dashboard.jsx      # Customer dashboard with active orders & order history
    │   ├── CheckoutPage.jsx   # Simulated payment screen (Demonstration mode)
    │   ├── PaymentSuccess.jsx # Post-payment confirmation receipt
    │   ├── AdminDashboard.jsx # Admin management: plan CRUD, orders table & CSV/PDF export
    │   ├── Login.jsx          # Sign-in form with SimpleJWT authentication
    │   ├── Signup.jsx         # Customer registration form
    │   ├── ForgotPassword.jsx # Password reset link request form
    │   ├── ResetPassword.jsx  # New password submission
    │   ├── About.jsx          # Information & company details
    │   ├── Contact.jsx        # Inquiries form submitting to Django ModelForm API
    │   └── NotFound.jsx       # 404 error page
    │
    ├── components/            # 🧩 Reusable UI Components
    │   ├── Navbar.jsx         # Sticky header with links, auth state & dark mode toggle
    │   ├── Footer.jsx         # Dual-variant footer (Customer and Admin views)
    │   ├── OrderTracker.jsx   # Visual delivery stage progress bar (Placed → Delivered)
    │   ├── Spinner.jsx        # Inline and full-page loading indicators
    │   ├── ProtectedRoute.jsx # Route guard requiring valid JWT authentication
    │   ├── AdminRoute.jsx     # Route guard requiring admin privileges
    │   ├── ToastContainer.jsx # Notification toast display
    │   └── chat/              # 💬 AI Assistant UI
    │       ├── ChatWidget.jsx        # Floating chatbot dialog with fullscreen toggle
    │       ├── MarkdownMessage.jsx   # Renders assistant responses with syntax formatting
    │       └── ChatErrorBoundary.jsx # Safeguard boundary for chat widget
    │
    ├── services/              # 🌐 Backend Communication Layer
    │   ├── api.js             # Axios instance with base URL /api & JWT Bearer interceptor
    │   ├── session.js         # Session cleanup (removes token & user on logout/expiry)
    │   └── chatStream.js      # Client for simulated typing assistant
    │
    ├── context/               # 🔄 Global State Providers
    │   ├── ThemeContext.jsx   # Dark / Light mode provider (synced to localStorage)
    │   ├── useTheme.jsx       # Hook to access theme state
    │   ├── ToastContext.jsx   # Toast notification provider
    │   └── useToast.jsx       # Hook to trigger toasts (success, error, info)
    │
    ├── hooks/                 # 🪝 Custom React Hooks
    │   └── useChat.js         # Chat message history, preference extraction & sending
    │
    ├── constants/             # 📌 Static Constants
    │   └── orderStatus.jsx    # Status definitions (Placed, Preparing, OutForDelivery, etc.)
    │
    └── utils/                 # 🛠️ Helper Utilities
        └── chatPreferences.js # Regex parser extracting budget, meal & duration preferences
```

---

## ⚡ Useful Commands

```bash
# Install dependencies
npm install

# Run Vite dev server (port 5173)
npm run dev

# Run production build
npm run build

# Run linter
npm run lint
```
