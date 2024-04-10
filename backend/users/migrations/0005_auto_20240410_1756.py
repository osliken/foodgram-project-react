# Generated by Django 3.2.16 on 2024-04-10 14:56

import django.core.validators
from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_subscribe_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscribe',
            options={'ordering': ('id',), 'verbose_name': 'Подписка на автора', 'verbose_name_plural': 'Подписки на автора'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, help_text='Введите имя пользователя', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Имя пользователя содержит недопустимый символ', regex='^[\\w.@+-]+$'), users.validators.validate_username], verbose_name='Имя пользователя'),
        ),
    ]
