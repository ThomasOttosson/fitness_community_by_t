from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as OriginalUserCreationForm
)
from django.contrib.auth.forms import (
    AuthenticationForm as OriginalAuthenticationForm
)
from .models import Review


# form for user reviews
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, str(i)) for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'comment': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'form-control',
                    'placeholder': 'Write your review here...'
                }
            ),
        }
        labels = {
            'rating': 'Your Rating',
            'comment': 'Your Comment',
        }


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
