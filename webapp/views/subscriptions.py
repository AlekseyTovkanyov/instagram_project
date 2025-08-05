from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View

from webapp.models import Subscription

User = get_user_model()


class ToggleSubscriptionView(LoginRequiredMixin, View):
    def post(self, request, pk):
        followed_user = get_object_or_404(User, pk=pk)
        if request.user == followed_user:
            return redirect('accounts:user_profile', pk=followed_user.pk)
        subscription, created = Subscription.objects.get_or_create(
            follower=request.user,
            followed=followed_user
        )
        if not created:
            subscription.delete()
        return redirect('accounts:user_profile', pk=followed_user.pk)
