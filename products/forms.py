from django import forms
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
