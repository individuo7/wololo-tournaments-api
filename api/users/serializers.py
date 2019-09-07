from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "icon",
            "gold",
            "background_color",
            "date_joined",
            "is_active",
            "last_login",
        ]
