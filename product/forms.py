from dj_rest_auth import forms
from .models import Rating


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('name', 'email', 'body')