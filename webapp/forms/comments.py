from django import forms
from django.forms import widgets

from webapp.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': widgets.Textarea(
                attrs={'placeholder': 'Добавьте комментарий...', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = False
