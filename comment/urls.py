from django.urls import path

from .views import CommentCreateView, CommentDetailView, CommentUpdateView, CommentDeleteView, CommentListView

urlpatterns = [
    path('create-comment/<int:pk>', CommentCreateView.as_view(), name='create_comment'),
    path('comments-list/<int:post_id>', CommentListView.as_view(), name='comments_list'),
    path('comment-detail/<int:pk>', CommentDetailView.as_view(), name='comment_detail'),
    path('comment-update/<int:pk>', CommentUpdateView.as_view(), name='comment_update'),
    path('comment-delete/<int:pk>', CommentDeleteView.as_view(), name='comment_delete'),
]
