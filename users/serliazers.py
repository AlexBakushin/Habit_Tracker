from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя.
    """
    class Meta:
        model = User
        fields = '__all__'
