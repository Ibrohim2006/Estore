from django import forms
from .models import NewsletterSubscriptionModel, CommentModel

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriptionModel
        fields = ['email']

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['message', 'name', 'email']
