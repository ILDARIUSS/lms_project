from django.urls import path

from users.views import (
    UserRetrieveUpdateAPIView,
    PaymentListCreateAPIView,
    PaymentRetrieveAPIView,
)

urlpatterns = [
    path('<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user_detail'),

    path('payments/', PaymentListCreateAPIView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_detail'),
]