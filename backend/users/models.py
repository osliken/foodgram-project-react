from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from recipes.constants import LENGTH_TEXT, MAX_LENGTH_EMAIL
from users.validators import validate_username


class User(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    email = models.EmailField(
        'Email',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        help_text='Введите адрес электронной почты',
        db_index=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        help_text='Введите имя пользователя',
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимый символ'
            ),
            validate_username
        ]
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        help_text='Введите ваше имя'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        help_text='Введите вашу фамилию'
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        help_text='Введите пароль'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='username_is_not_me'
            )
        ]

    def __str__(self):
        return self.username[:LENGTH_TEXT]


class Subscribe(models.Model):
    """Модель подписки на автора рецепта."""

    subscriber = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscribers',
        help_text='Выберите подписчика'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='authors',
        help_text='Выберите автора'
    )

    class Meta:
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на автора'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'subscriber'],
                name='unique_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.author}'
