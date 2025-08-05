from django import forms


class UserSearchForm(forms.Form):
    search = forms.CharField(max_length=50, label='Поиск пользователей', required=False)
