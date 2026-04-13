from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='имя')
    last_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='фамилия')

    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='город')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'

    PAYMENT_METHOD_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='пользователь'
    )
    payment_date = models.DateTimeField(verbose_name='дата оплаты')
    paid_course = models.ForeignKey(
        'materials.Course',
        on_delete=models.CASCADE,
        related_name='course_payments',
        blank=True,
        null=True,
        verbose_name='оплаченный курс'
    )
    paid_lesson = models.ForeignKey(
        'materials.Lesson',
        on_delete=models.CASCADE,
        related_name='lesson_payments',
        blank=True,
        null=True,
        verbose_name='оплаченный урок'
    )
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='способ оплаты'
    )

    def __str__(self):
        return f'{self.user} - {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['-payment_date']