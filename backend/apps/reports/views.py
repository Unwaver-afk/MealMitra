import csv
import io
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import APIView
from orders.models import Order
from accounts.permissions import IsAdminRole
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.utils import timezone


class ExportOrdersCSVView(APIView):
    """
    GET /api/reports/orders/csv/
    Generates a CSV report of all orders using Python's built-in csv module (Module 6).
    """
    permission_classes = [IsAdminRole]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="mealmitra_orders_{timestamp}.csv"'

        writer = csv.writer(response)
        # Header Row
        writer.writerow([
            'Order ID',
            'Customer Name',
            'Customer Email',
            'Plan Title',
            'Meal Type',
            'Duration',
            'Price (INR)',
            'Payment Status',
            'Order Status',
            'Order Date'
        ])

        orders = Order.objects.all().select_related('user', 'plan').order_by('-created_at')
        for order in orders:
            writer.writerow([
                order.id,
                order.user.name,
                order.user.email,
                order.plan.title,
                order.plan.meal_type,
                order.plan.duration,
                float(order.plan.price),
                order.payment_status,
                order.order_status,
                order.created_at.strftime('%Y-%m-%d %H:%M')
            ])

        return response


class ExportOrdersPDFView(APIView):
    """
    GET /api/reports/orders/pdf/
    Generates a PDF summary report of customer orders using ReportLab (Module 6).
    """
    permission_classes = [IsAdminRole]

    def get(self, request):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(letter),
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )
        elements = []
        styles = getSampleStyleSheet()

        # Custom Styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#059669'), # Emerald theme
            spaceAfter=6,
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=15,
        )

        # Title and metadata
        elements.append(Paragraph("MealMitra — Customer Orders Report", title_style))
        report_time = timezone.now().strftime('%d %B %Y, %I:%M %p')
        elements.append(Paragraph(f"Generated on {report_time} | Full Stack Development Lab Evaluation", subtitle_style))
        elements.append(Spacer(1, 10))

        # Table Data
        table_data = [
            ['ID', 'Customer', 'Email', 'Plan Title', 'Meal Type', 'Duration', 'Price', 'Payment', 'Status']
        ]

        orders = Order.objects.all().select_related('user', 'plan').order_by('-created_at')[:50]
        for o in orders:
            table_data.append([
                f"#{o.id}",
                o.user.name[:18],
                o.user.email[:22],
                o.plan.title[:20],
                o.plan.meal_type,
                o.plan.duration,
                f"₹{int(o.plan.price)}",
                o.payment_status,
                o.order_status
            ])

        # Table Styling
        order_table = Table(table_data, colWidths=[40, 100, 130, 110, 65, 65, 55, 65, 80])
        order_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8.5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements.append(order_table)
        doc.build(elements)

        buffer.seek(0)
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="mealmitra_orders_{timestamp}.pdf"'
        return response
