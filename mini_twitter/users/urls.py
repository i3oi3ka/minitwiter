from django.urls import path
from django.contrib.auth import views as auth_views

from .views import RegisterView, ChangeProfile, ChangeInfo, UserDetail, subscribe, unsubscribe, password_reset_request
from .views import login_view, logout_view, UserList

urlpatterns = [
    path('user_list/', UserList.as_view(), name='users_list'),
    path('user-detail/<int:pk>', UserDetail.as_view(), name='user_detail'),
    path('auth/sign-up/', RegisterView.as_view(), name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('change-user-info/<int:pk>', ChangeInfo.as_view(), name='change_user_info'),
    path('change-profile/<int:pk>', ChangeProfile.as_view(), name='change_profile'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/p_r_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/r_token.html'),
         name='password_reset_confirm'),
    path('reset/done',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/r_done.html'),
         name='password_reset_complete'),
]
