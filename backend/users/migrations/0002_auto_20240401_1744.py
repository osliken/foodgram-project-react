# Generated by Django 3.2.15 on 2024-04-01 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
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
    ]
