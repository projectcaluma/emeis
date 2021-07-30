from django.contrib.auth.models import AnonymousUser
from rest_framework_json_api import serializers

from .models import ACL, Permission, Role, Scope, User


class BaseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    created_by_user = serializers.ResourceRelatedField(read_only=True)

    def create(self, validated_data):
        user = self.context["request"].user
        if not isinstance(user, AnonymousUser):
            validated_data["created_by_user"] = user.user

        return super().create(validated_data)

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)
        self.Meta.model.check_permissions(self.context["request"])
        if self.instance is not None:
            self.instance.check_object_permissions(self.context["request"])

        return validated_data

    class Meta:
        fields = ("created_at", "modified_at", "created_by_user", "meta")


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
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "language",
            "address",
            "city",
            "zip",
            "acls",
            "is_active",
            "date_joined",
            "modified_at",
            "created_at",
            "created_by_user",
            "meta",
        ]


class ScopeSerializer(BaseSerializer):
    class Meta:
        model = Scope
        fields = BaseSerializer.Meta.fields + ("name", "description", "parent", "level")


class PermissionSerializer(BaseSerializer):
    class Meta:
        model = Permission
        fields = BaseSerializer.Meta.fields + ("slug", "name", "description", "roles")


class RoleSerializer(BaseSerializer):
    permissions = serializers.ResourceRelatedField(
        queryset=Permission.objects.all(), required=False, many=True
    )
    included_serializers = {
        "permissions": PermissionSerializer,
    }

    class Meta:
        model = Role
        fields = BaseSerializer.Meta.fields + (
            "slug",
            "name",
            "description",
            "permissions",
        )


class ACLSerializer(BaseSerializer):
    included_serializers = {
        "user": UserSerializer,
        "scope": ScopeSerializer,
        "role": RoleSerializer,
    }

    class Meta:
        model = ACL
        fields = "__all__"
