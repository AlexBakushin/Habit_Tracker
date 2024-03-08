from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.serliazers import UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status
from main.permissions import IsOwnerOrModerator, IsModer, IsOwner


class UserViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для работы с пользователями
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        """
        Ограничения режимами доступа
        """
        if self.action == 'create':
            self.permission_classes = [~IsModer]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner, ~IsModer & IsOwner]

        return [permission() for permission in self.permission_classes]
