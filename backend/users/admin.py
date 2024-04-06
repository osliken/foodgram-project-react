from django.contrib import admin
from foodgram.settings import LIST_PER_PAGE

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Раздел пользователей."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'is_admin'
    )
    empty_value_display = 'значение отсутствует'
    list_editable = ('is_admin',)
    list_filter = ('username', 'email')
    list_per_page = LIST_PER_PAGE
    search_fields = ('username',)


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
    search_fields = ('author',)


admin.site.site_title = 'Администрирование Foodgram'
admin.site.site_header = 'Администрирование Foodgram'
