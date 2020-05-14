from rest_framework_json_api import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = User.REQUIRED_FIELDS + [User.USERNAME_FIELD]
