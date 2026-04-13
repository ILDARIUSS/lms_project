from django.urls import path

from users.views import (
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    PaymentListCreateAPIView,
    PaymentRetrieveAPIView,
)

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('', UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),

    path('payments/', PaymentListCreateAPIView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_detail'),
]