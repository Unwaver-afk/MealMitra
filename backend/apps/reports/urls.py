from django.urls import path
from .views import ExportOrdersCSVView, ExportOrdersPDFView

urlpatterns = [
    path('orders/csv', ExportOrdersCSVView.as_view(), name='export-orders-csv'),
    path('orders/csv/', ExportOrdersCSVView.as_view(), name='export-orders-csv-slash'),
    path('orders/pdf', ExportOrdersPDFView.as_view(), name='export-orders-pdf'),
    path('orders/pdf/', ExportOrdersPDFView.as_view(), name='export-orders-pdf-slash'),
]
