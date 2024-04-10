from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers.users import UserGETSerializer
from recipes.constants import MAX_INGREDIENT, MIN_INGREDIENT
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор создания объектов для модели IngredientRecipe."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')

    def validate(self, data):
        if data.get('amount') < MIN_INGREDIENT:
            raise serializers.ValidationError(
                'Количество ингредиентов не может быть меньше '
                f'{MIN_INGREDIENT}'
            )
        if data.get('amount') > MAX_INGREDIENT:
            raise serializers.ValidationError(
                'Количество ингредиентов не может быть больше '
                f'{MAX_INGREDIENT}'
            )
        return data


class IngredientFullSerializer(serializers.ModelSerializer):
    """Сериализатор для модели IngredientRecipe."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeGETSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipe для GET запросов."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserGETSerializer(read_only=True)
    ingredients = IngredientFullSerializer(
        many=True, source='ingredient_recipes'
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, object):
        """Проверка добавления рецепта в избранное."""
        request = self.context.get('request')
        return (
            request is not None and request.user.is_authenticated
            and request.user.favoritings.filter(recipe=object).exists()
        )

    def get_is_in_shopping_cart(self, object):
        """Проверка добавления рецепта в список покупок."""
        request = self.context.get('request')
        return (
            request is not None and request.user.is_authenticated
            and request.user.shopping_carts.filter(recipe=object).exists()
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipe для небезопасных запросов."""

    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField()
    author = UserGETSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author'
        )

    def validate(self, data):
        if not data.get('ingredients'):
            raise serializers.ValidationError(
                'Нужно указать минимум 1 ингредиент'
            )
        ingredients_data = [
            ingredient.get('id') for ingredient in data.get('ingredients')
        ]
        if len(ingredients_data) != len(set(ingredients_data)):
            raise serializers.ValidationError(
                'Ингредиенты рецепта должны быть уникальными'
            )
        if not data.get('tags'):
            raise serializers.ValidationError(
                'Нужно указать минимум 1 тег'
            )
        if not data.get('image'):
            raise serializers.ValidationError(
                'Нужно добавить изображение'
            )
        return data

    def validate_tags(self, tags):
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                'Теги рецепта должны быть уникальными'
            )
        return tags

    @staticmethod
    def add_ingredients(ingredients_data, recipe):
        IngredientRecipe.objects.bulk_create([
            IngredientRecipe(
                ingredient=ingredient.get('id'),
                recipe=recipe,
                amount=ingredient.get('amount')
            )
            for ingredient in ingredients_data
        ])

    @transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        recipe = instance
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.add_ingredients(ingredients, recipe)
        return super().update(instance, validated_data)

    def to_representation(self, recipe):
        request = self.context.get('request')
        serializer = RecipeGETSerializer(recipe, context={'request': request})
        return serializer.data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для компактного отображения рецептов."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Favorite и ShoppingCart."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Вы уже добавляли это рецепт в избранное'
            )
        ]

    def validate(self, data):
        recipe = data.get('recipe')
        if not Recipe.objects.filter(id=recipe.id).exists():
            raise serializers.ValidationError(
                'Рецепт не найден'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        serializer = RecipeShortSerializer(
            instance.recipe, context={'request': request}
        )
        return serializer.data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ShoppingCart."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Вы уже добавляли это рецепт в список покупок'
            )
        ]

    def validate(self, data):
        recipe = data.get('recipe')
        if not Recipe.objects.filter(id=recipe.id).exists():
            raise serializers.ValidationError(
                'Рецепт не найден'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        serializer = RecipeShortSerializer(
            instance.recipe, context={'request': request}
        )
        return serializer.data
