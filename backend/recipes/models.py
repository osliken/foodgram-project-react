from colorfield.fields import ColorField
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)
from django.db import models

from foodgram.settings import LENGTH_TEXT
from users.models import User


class Tag(models.Model):
    """Модель тега для рецепта."""

    name = models.CharField(
        'Имя тега',
        max_length=200,
        unique=True,
        help_text='Введите имя тега',
        db_index=True
    )
    color = ColorField(
        'Цвет тега',
        max_length=7,
        unique=True,
        help_text='Выберите цвет'
    )
    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True,
        help_text='Укажите слаг',
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг тега содержит недопустимый символ'
        )]
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.slug[:LENGTH_TEXT]


class Ingredient(models.Model):
    """Модель ингредиента для рецепта."""

    name = models.CharField(
        'Наименование ингредиента',
        max_length=200,
        help_text='Введите наименование ингредиента',
        db_index=True
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        help_text='Введите единицу измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class Recipe(models.Model):
    """Модель рецепта блюда."""

    name = models.CharField(
        'Название рецепта',
        max_length=200,
        help_text='Введите название рецепта',
        db_index=True
    )
    image = models.ImageField(
        'Изображение блюда',
        upload_to='recipes/',
        help_text='Добавьте изображение готового блюда'
    )
    text = models.TextField(
        'Описание рецепта',
        help_text='Опишите способ приготовления блюда'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        help_text='Введите время приготовления блюда в минутах',
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления не может быть меньше минуты'
            )
        ]
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text='Выберите автора рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='IngredientRecipe',
        related_name='recipes',
        help_text='Выберите ингредиент'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
        help_text='Выберите тег'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class IngredientRecipe(models.Model):
    """Модель для связи Ingredient и Recipe."""

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
        help_text='Выберите ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
        help_text='Выберите рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        help_text='Укажите количество выбранного ингредиента',
        validators=[
            MinValueValidator(
                1,
                message='Количество ингредиента не может быть меньше одного'
            ),
            MaxValueValidator(
                1000,
                message='Количество ингредиента не может быть больше тысячи'
            )
        ]
    )

    class Meta:
        verbose_name = 'Соответствие рецепта и ингредиента'
        verbose_name_plural = 'Соответствие рецептов и ингредиентов'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe} содержит ингредиенты: {self.ingredient}'


class Favorite(models.Model):
    """Модель для добавления рецептов в избранное."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favoriting',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Избранный рецепт',
        on_delete=models.CASCADE,
        related_name='favoriting',
        help_text='Выберите рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class ShoppingCart(models.Model):
    """Модель для списка покупок пользователя."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт для списка покупок',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        help_text='Выберите рецепт для списка покупок'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'
