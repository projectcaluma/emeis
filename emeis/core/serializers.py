from rest_framework_json_api import serializers

from .models import ACL, Permission, Role, Scope, User


class BaseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    created_by_user = serializers.ResourceRelatedField(read_only=True)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by_user"] = user

        return super().create(validated_data)

    class Meta:
        fields = ("created_at", "modified_at", "created_by_user")


class MeSerializer(BaseSerializer):
    acls = serializers.ResourceRelatedField(many=True, read_only=True)
    included_serializers = {
        "acls": "emeis.core.serializers.ACLSerializer",
    }

    class Meta:
        model = User
        fields = "__all__"


class MyACLSerializer(BaseSerializer):
    included_serializers = {
        "scope": "emeis.core.serializers.ScopeSerializer",
        "role": "emeis.core.serializers.RoleSerializer",
    }

    class Meta:
        model = ACL
        fields = "__all__"


class UserSerializer(BaseSerializer):
    acls = serializers.ResourceRelatedField(many=True, read_only=True)

    included_serializers = {
        "acls": "emeis.core.serializers.ACLSerializer",
    }

    class Meta:
        model = User
        fields = "__all__"


class ScopeSerializer(BaseSerializer):
    class Meta:
        model = Scope
        fields = BaseSerializer.Meta.fields + ("name", "description", "parent")


class PermissionSerializer(BaseSerializer):
    class Meta:
        model = Permission
        fields = BaseSerializer.Meta.fields + ("name", "description")


class RoleSerializer(BaseSerializer):
    included_serializers = {
        "permissions": PermissionSerializer,
    }

    class Meta:
        model = Role
        fields = BaseSerializer.Meta.fields + ("name", "description", "permissions")


class ACLSerializer(BaseSerializer):
    included_serializers = {
        "user": UserSerializer,
        "scope": ScopeSerializer,
        "role": RoleSerializer,
    }

    class Meta:
        model = ACL
        fields = "__all__"
