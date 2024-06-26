# Generated by Django 3.2.16 on 2024-04-07 18:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0006_auto_20240405_2058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Избранный рецепт', 'verbose_name_plural': 'Избранные рецепты'},
        ),
        migrations.AlterModelOptions(
            name='ingredientrecipe',
            options={'verbose_name': 'Соответствие рецепта и ингредиента', 'verbose_name_plural': 'Соответствие рецептов и ингредиентов'},
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(help_text='Выберите рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='favoritings', to='recipes.recipe', verbose_name='Избранный рецепт'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(help_text='Выберите пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='favoritings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(help_text='Укажите количество выбранного ингредиента', validators=[django.core.validators.MinValueValidator(1, 'Количество ингредиента не может быть меньше 1'), django.core.validators.MaxValueValidator(1000, 'Количество ингредиента не может быть больше 1000')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(help_text='Выберите ингредиент', on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recipes', to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(help_text='Выберите рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recipes', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='Введите время приготовления блюда в минутах', validators=[django.core.validators.MinValueValidator(1, 'Время приготовления не может быть меньше 1 мин.'), django.core.validators.MaxValueValidator(1440, 'Время приготовления не может быть больше 1440 мин.')], verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(help_text='Выберите рецепт для списка покупок', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_carts', to='recipes.recipe', verbose_name='Рецепт для списка покупок'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(help_text='Выберите пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_carts', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(help_text='Укажите слаг', max_length=200, unique=True, verbose_name='Слаг'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_name_measurement_unit'),
        ),
    ]
