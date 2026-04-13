from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User, Payment
from users.permissions import IsProfileOwner
from users.serializers import (
    UserListSerializer,
    UserPublicProfileSerializer,
    UserOwnProfileSerializer,
    UserRegisterSerializer,
    PaymentSerializer,
    CustomTokenObtainPairSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user_object = self.get_object()
        if self.request.user == user_object:
            return UserOwnProfileSerializer
        return UserPublicProfileSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserOwnProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserOwnProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]


class PaymentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)