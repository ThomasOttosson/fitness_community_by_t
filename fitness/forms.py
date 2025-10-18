from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as OriginalUserCreationForm
)
from django.contrib.auth.forms import (
    AuthenticationForm as OriginalAuthenticationForm
)


# email subscription form
class NewsletterForm(forms.Form):
    email = forms.EmailField(
        label='',  # Empty label for cleaner UI
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your email address',
                'required': 'true'
            }
        )
    )


# Custom UserCreationForm - styled registration form
class CustomUserCreationForm(OriginalUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class and placeholder to all fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',  # Added placeholder
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',  # Added placeholder
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password Confirmation',
        })


# styled login form
class CustomAuthenticationForm(OriginalAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',  # Added placeholder
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',  # Added placeholder
        })
