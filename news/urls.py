from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostListView.as_view(), name="post-list"),
    path("posts/featured/", views.FeaturedPostView.as_view(), name="post-featured"),
    path("posts/<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
    path("tags/", views.TagListView.as_view(), name="tag-list"),
    path("subscribe/", views.SubscribeView.as_view(), name="subscribe"),
    path("unsubscribe/", views.UnsubscribeView.as_view(), name="unsubscribe"),
]
