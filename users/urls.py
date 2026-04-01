from django.urls import path

from users.views import UserRetrieveUpdateAPIView

urlpatterns = [
    path('<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user_detail'),
]