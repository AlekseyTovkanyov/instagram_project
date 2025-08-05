from django.urls import path
from django.views.generic import RedirectView

from webapp.views import ToggleLikeView
from webapp.views.subscriptions import ToggleSubscriptionView
from webapp.views.posts import PostListView, PostCreateView, PostDetailView, PostCommentView

app_name = 'webapp'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='webapp:index')),
    path('posts/', PostListView.as_view(), name='index'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('subscribe/<int:pk>/', ToggleSubscriptionView.as_view(), name='toggle_subscription'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/like/', ToggleLikeView.as_view(), name='toggle_like'),
    path('post/<int:pk>/comment/', PostCommentView.as_view(), name='post_comment'),
]
