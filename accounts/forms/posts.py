from django import forms
from django.forms import widgets

from webapp.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'description']
        widgets = {
            'description': widgets.Textarea(attrs={"cols": 24, "rows": 5}),
        }
