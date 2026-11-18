from django import forms
from plans.models import TiffinPlan, Tag


class TiffinPlanModelForm(forms.ModelForm):
    """
    Demonstrates Django ModelForm with field widgets, error messages, and clean methods.
    Module 4 requirement.
    """
    class Meta:
        model = TiffinPlan
        fields = ['title', 'meal_type', 'duration', 'price', 'tags', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Special Sunday Biryani'}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Price in INR', 'step': '0.01'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '4'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Nutritional details and dishes included...'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 1:
            raise forms.ValidationError("Price must be at least ₹1.")
        return price

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long.")
        return title

