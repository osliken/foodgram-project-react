from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from ..filters import IngredientSearchFilter, RecipeFilter
from ..permissions import AuthorOrReadOnly
from ..serializers.recipes import (FavoriteSerializer, IngredientSerializer,
                                   RecipeGETSerializer, RecipeSerializer,
                                   RecipeShortSerializer,
                                   ShoppingCartSerializer, TagSerializer)
from ..utils import create_shopping_cart


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Tag."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Ingredient."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Recipe."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, AuthorOrReadOnly
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitOffsetPagination

    @action(
        detail=True,
        methods=['post'],
        url_path='favorite',
        url_name='favorite',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk):
        """Позволяет пользователю добавлять рецепты в избранное."""
        if not Recipe.objects.filter(pk=pk).exists():
            return Response(
                'Рецепт не найден', status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = FavoriteSerializer(
            data={'user': request.user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        favorite_serializer = RecipeShortSerializer(recipe)
        return Response(
            favorite_serializer.data, status=status.HTTP_201_CREATED
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Позволяет пользователю удалять рецепты из избранного."""
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite_recipe = request.user.favoritings.filter(recipe=recipe)
        if not favorite_recipe.exists():
            return Response(
                'Рецепт не найден', status=status.HTTP_400_BAD_REQUEST
            )
        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """Позволяет пользователю добавлять рецепты
        в список покупок."""
        if not Recipe.objects.filter(pk=pk).exists():
            return Response(
                'Рецепт не найден', status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = ShoppingCartSerializer(
            data={'user': request.user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        shopping_cart_serializer = RecipeShortSerializer(recipe)
        return Response(
            shopping_cart_serializer.data, status=status.HTTP_201_CREATED
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Позволяет пользователю удалять рецепты
        из списка покупок."""
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_cart_recipe = request.user.shopping_carts.filter(
            recipe=recipe
        )
        if not shopping_cart_recipe.exists():
            return Response(
                'Рецепт не найден', status=status.HTTP_400_BAD_REQUEST
            )
        shopping_cart_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Позволяет текущему пользователю загрузить список покупок."""
        ingredients_cart = (
            IngredientRecipe.objects.filter(
                recipe__shopping_carts__user=request.user
            ).values(
                'ingredient__name',
                'ingredient__measurement_unit',
            ).order_by(
                'ingredient__name'
            ).annotate(ingredient_value=Sum('amount'))
        )
        return create_shopping_cart(ingredients_cart)

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return RecipeGETSerializer
        return RecipeSerializer
