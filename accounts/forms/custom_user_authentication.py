from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Логин или Email")

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email and password:
            try:
                user_obj = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
                self.user_cache = authenticate(self.request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                self.user_cache = None

            if self.user_cache is None:
                raise forms.ValidationError("Неверный логин/email или пароль")
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
