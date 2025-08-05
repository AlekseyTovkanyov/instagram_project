from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'password1', 'password2', 'first_name', 'bio', 'phone_number',
                  'gender']
        widgets = {
            'bio': widgets.Textarea(attrs={"cols": 24, "rows": 5}),
            'gender': widgets.Select()
        }
