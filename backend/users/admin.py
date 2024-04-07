from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from recipes.constants import LIST_PER_PAGE

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Раздел пользователей."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'count_recipes',
        'count_subscribers'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('username', 'email')
    list_per_page = LIST_PER_PAGE
    search_fields = ('username',)

    @admin.display(description='Количество рецептов')
    def count_recipes(self, object):
        """Вычисляет количество рецептов у автора."""
        return object.recipes.count()

    @admin.display(description='Количество подписчиков')
    def count_subscribers(self, object):
        """Вычисляет количество подписчиков у автора."""
        return object.authors.count()


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Раздел подписок."""

    list_display = (
        'pk',
        'author',
        'subscriber',
    )

    list_editable = ('author', 'subscriber')
    list_filter = ('author',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('author__username',)


admin.site.site_title = 'Администрирование Foodgram'
admin.site.site_header = 'Администрирование Foodgram'
