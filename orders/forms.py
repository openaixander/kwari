from django import forms    
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name',
            'phone_number',
            'delivery_address',
            'order_note'
            ]
        
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'John Doe'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'order_note': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }