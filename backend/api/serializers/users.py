from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Subscribe, User


class UserSerializer(UserCreateSerializer):
    """Сериализатор для создания объекта модели User."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data


class UserGETSerializer(UserSerializer):
    """Сериализатор для модели User."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )

    def get_is_subscribed(self, object):
        """Проверка подписки пользователя на автора."""
        request = self.context.get('request')
        return (
            request is None or not request.user.is_authenticated
            or object.authors.filter(subscriber=request.user).exists()
        )


class SubscribeShowSerializer(UserGETSerializer):
    """Сериализатор отображения подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserGETSerializer):
        model = User
        fields = UserGETSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, object):
        from api.serializers.recipes import RecipeShortSerializer
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        recipes = object.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShortSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, object):
        return object.recipes.count()


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Subscribe."""

    class Meta:
        model = Subscribe
        fields = ('author', 'subscriber')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('author', 'subscriber'),
                message='Вы уже подписывались на этого автора'
            )
        ]

    def validate(self, data):
        if data['subscriber'] == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return SubscribeShowSerializer(
            instance.author, context={'request': request}
        ).data
