from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Subscribe, User

from ..pagination import PageLimitPagination
from ..permissions import AnonimOrAuthenticatedReadOnly
from ..serializers.users import (
    CustomUserSerializer,
    SubscribeSerializer,
    SubscribeShowSerializer
)


class CustomUserViewSet(UserViewSet):
    """Вьюсет модели User."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AnonimOrAuthenticatedReadOnly,)
    pagination_class = PageLimitPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me(self, request):
        """Позволяет пользователю получить подробную информацию о себе
        и редактировать её."""
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(
            request.user, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        url_path='subscribe',
        url_name='subscribe',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, id):
        """Позволяет пользователю подписываться на автора."""
        author = get_object_or_404(User, id=id)
        serializer = SubscribeSerializer(
            data={'subscriber': request.user.id, 'author': author.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        author_serializer = SubscribeShowSerializer(
            author, context={'request': request}
        )
        return Response(
            author_serializer.data, status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        """Позволяет пользователю отписываться от автора."""
        author = get_object_or_404(User, id=id)
        subscription = Subscribe.objects.filter(
            subscriber=request.user, author=author
        )
        if not subscription.exists():
            return Response(
                'Подписка не найдена', status=status.HTTP_400_BAD_REQUEST
            )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions',
        url_name='subscriptions',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_subscriptions(self, request):
        """Возвращает авторов, на которых подписан пользователь."""
        authors = User.objects.filter(author__subscriber=request.user)
        paginator = PageLimitPagination()
        result_pages = paginator.paginate_queryset(
            queryset=authors, request=request
        )
        serializer = SubscribeShowSerializer(
            result_pages, context={'request': request}, many=True
        )
        return paginator.get_paginated_response(serializer.data)
