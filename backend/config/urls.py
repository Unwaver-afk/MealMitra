from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.conf.urls.static import static


def root_view(request):
    return HttpResponse("MealMitra API running (Python Django Backend)", content_type="text/plain")


def health_view(request):
    return JsonResponse({"status": "ok", "backend": "Python Django", "database": "SQLite"})


urlpatterns = [
    # Server Root & Health
    path('', root_view, name='root'),
    path('health', health_view, name='health'),
    path('health/', health_view, name='health-slash'),

    # Django Admin
    path('admin/', admin.site.urls),

    # REST APIs for MealMitra
    path('api/auth/', include('accounts.urls')),
    path('api/plans/', include('plans.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/payment/', include('payments.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/contact/', include('contact.urls')),

    # College Syllabus Lab Demonstration Section (MVT, Templates, DTL, Forms)
    path('lab-demo/', include('lab_demo.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
