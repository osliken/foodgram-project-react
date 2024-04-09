from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as UserView
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.pagination import PageLimitPagination
from api.permissions import AdminOrReadOnly
from api.serializers.users import (SubscribeSerializer,
                                   SubscribeShowSerializer,
                                   UserGETSerializer)
from users.models import Subscribe, User


class UserViewSet(UserView):
    """Вьюсет модели User."""

    queryset = User.objects.all()
    serializer_class = UserGETSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageLimitPagination

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me(self, request):
        if request.method == 'PATCH':
            serializer = UserGETSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserGETSerializer(
            request.user, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=('POST',),
        url_path='subscribe',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        serializer = SubscribeSerializer(
            data={'subscriber': request.user.id, 'author': author.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        subscription = Subscribe.objects.filter(
            subscriber=request.user, author=author
        )
        if not subscription.exists():
            return Response(
                {'errors': 'Подписка не найдена'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('GET',),
        url_path='subscriptions',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        authors = User.objects.filter(authors__subscriber=request.user)
        paginator = PageLimitPagination()
        result_pages = paginator.paginate_queryset(
            queryset=authors, request=request
        )
        serializer = SubscribeShowSerializer(
            result_pages, context={'request': request}, many=True
        )
        return paginator.get_paginated_response(serializer.data)
