from django.urls import path

from .views import PostListView, PostCreateView, PostDetailView, \
    like, PostUpdateView, PostDeleteView, LikedPostUserList, PostUserListView

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list'),
    path('posts_list/<str:folder>', PostListView.as_view(), name='posts_list'),
    path('like/<int:pk>', like, name='like'),
    path('liked_post_user/<int:pk>', LikedPostUserList.as_view(), name='liked_post_user'),
    path('posts_list_user/<int:user_id>', PostUserListView.as_view(), name='posts_list_user'),
    path('create-post/', PostCreateView.as_view(), name='create_post'),
    path('update-post/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete-post/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('post-detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),


]
