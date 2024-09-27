from django.urls import path
from . import views

urlpatterns = [
    path('home-feed/', views.HomeFeed.as_view(), name='home-feed'),
    path('create-post/', views.CreatePost.as_view(), name='create-post'),
    path('post-details/<str:post_id>/', views.PostDetails.as_view(), name='post-details'),
    path('create-comment/<str:post_id>/', views.CreateComment.as_view(), name='create-comment'),
    path('comment-details/<str:comment_id>/', views.CommentDetails.as_view(), name='comment-details'),
]
