from django.contrib import admin
from recipes.constants import LIST_PER_PAGE

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Раздел тегов."""

    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Раздел ингредиентов."""

    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name',)


class IngredientRecipeInline(admin.TabularInline):
    """Добавить ингредиенты в рецепты."""

    model = IngredientRecipe
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Раздел рецептов."""

    list_display = (
        'pk',
        'name',
        'author',
        'text',
        'get_tags',
        'get_ingredients',
        'cooking_time',
        'image',
        'pub_date',
        'count_favorite',
    )
    inlines = [
        IngredientRecipeInline,
    ]

    empty_value_display = 'значение отсутствует'
    list_editable = ('author',)
    list_filter = ('author', 'name', 'tags')
    list_per_page = LIST_PER_PAGE
    search_fields = ('author__username', 'name')

    @admin.display(description='ингредиенты')
    def get_ingredients(self, object):
        """Получает ингредиент или список ингредиентов рецепта."""
        return '\n'.join(
            (ingredient.name for ingredient in object.ingredients.all())
        )

    @admin.display(description='теги')
    def get_tags(self, object):
        """Получает тег или список тегов рецепта."""
        return '\n'.join((tag.name for tag in object.tags.all()))

    @admin.display(description='Количество добавлений в избранное')
    def count_favorite(self, object):
        """Вычисляет количество добавлений рецепта в избранное."""
        return object.favoritings.count()


@admin.register(IngredientRecipe)
class IngredientRecipetAdmin(admin.ModelAdmin):
    """Cоответствие игредиентов и рецептов."""

    list_display = (
        'pk',
        'ingredient',
        'amount',
        'recipe'
    )
    empty_value_display = 'значение отсутствует'
    list_per_page = LIST_PER_PAGE


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Раздел избранного."""

    list_display = (
        'pk',
        'user',
        'recipe',
    )

    empty_value_display = 'значение отсутствует'
    list_editable = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user__username',)
    list_per_page = LIST_PER_PAGE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Раздел рецептов, которые добавлены в список покупок."""

    list_display = (
        'pk',
        'user',
        'recipe',
    )

    empty_value_display = 'значение отсутствует'
    list_editable = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user__username',)
    list_per_page = LIST_PER_PAGE
