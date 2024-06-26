from django.urls import include, path
from rest_framework import routers

from api.views.recipes import IngredientViewSet, RecipeViewSet, TagViewSet
from api.views.users import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
