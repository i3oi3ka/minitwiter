from django.urls import path
from .views import MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView, MessageListView

urlpatterns = [
    path('message_create/<int:pk>', MessageCreateView.as_view(), name='message_create'),
    path('message_detail/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message_update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('message_list/<str:folder>', MessageListView.as_view(), name='message_list'),
]

