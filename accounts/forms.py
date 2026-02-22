from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    # We define the fields explicitly to add styling/placeholders
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input', 
            'placeholder': 'example@email.com',
            'id': 'email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input', 
            'placeholder': 'Create a strong password',
            'id': 'password'
        }),
        validators=[validate_password] # Django's built-in strength checker
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input', 
            'placeholder': 'Re-enter your password',
            'id': 'confirmPassword'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def clean_email(self):
        # Automatic Unique Check
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        # Automatic Password Match Check
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data