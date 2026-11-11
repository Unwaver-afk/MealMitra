from django.db import models


class ContactMessage(models.Model):
    """
    Model for handling customer contact inquiries.
    Used to demonstrate Django Forms, ModelForms, and server-side validation.
    """
    name = models.CharField('Full Name', max_length=100)
    email = models.EmailField('Email Address')
    subject = models.CharField('Subject', max_length=200, default='General Inquiry')
    message = models.TextField('Message', max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} <{self.email}>: {self.subject}"
