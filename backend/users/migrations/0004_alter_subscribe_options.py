# Generated by Django 3.2.16 on 2024-04-09 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20240407_2302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscribe',
            options={'verbose_name': 'Подписка на автора', 'verbose_name_plural': 'Подписки на автора'},
        ),
    ]