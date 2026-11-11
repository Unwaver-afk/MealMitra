from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import ContactForm
from .models import ContactMessage


class ContactAPIView(APIView):
    """
    POST /api/contact/
    Receives contact messages, validates using Django ModelForm, and stores them in SQLite.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        form = ContactForm(data=request.data)
        if form.is_valid():
            contact_msg = form.save()
            return Response({
                "success": True,
                "message": "Thank you for reaching out! We have received your inquiry.",
                "id": contact_msg.id
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "errors": form.errors
        }, status=status.HTTP_400_BAD_REQUEST)
