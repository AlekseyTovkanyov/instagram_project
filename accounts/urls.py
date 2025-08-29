from django.urls import path

from accounts.views import RegistrationView, UserDetailView, CustomLoginView, CustomLogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_profile')
]
