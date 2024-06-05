from django.contrib.auth.models import AnonymousUser
from generic_permissions.validation import ValidatorMixin
from rest_framework_json_api import serializers

from .models import ACL, Permission, Role, Scope, User


class BaseSerializer(ValidatorMixin, serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    created_by_user = serializers.ResourceRelatedField(read_only=True)

    def create(self, validated_data):
        user = self.context["request"].user
        if not isinstance(user, AnonymousUser):
            validated_data["created_by_user"] = user.user

        return super().create(validated_data)

    class Meta:
        fields = ("created_at", "modified_at", "created_by_user", "metainfo")


class MeSerializer(BaseSerializer):
    acls = serializers.ResourceRelatedField(many=True, read_only=True)
    included_serializers = {
        "acls": "emeis.core.serializers.ACLSerializer",
    }

    class Meta:
        model = User
        fields = "__all__"


class MyACLSerializer(BaseSerializer):
    scope = serializers.ResourceRelatedField(
        queryset=Scope.objects.all(), required=False, many=False
    )

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
            "metainfo",
        ]


class ScopeSerializer(BaseSerializer):
    level = serializers.SerializerMethodField()

    def get_level(self, obj):
        depth = getattr(obj, "tree_depth", None)
        if depth is not None:
            return depth

        # Note: This should only happen on CREATE, never in GET (Either list,
        # detail, or include!) In CREATE, it's a new object that doesn't come
        # from a QS

        # Sometimes, the model object may come out of a non-django-tree-queries
        # QS, and thus would not have the `tree_*` attributes amended. Then we
        # need to go the "slow path"
        return obj.ancestors().count()

    class Meta:
        model = Scope
        fields = BaseSerializer.Meta.fields + (
            "name",
            "description",
            "parent",
            "level",
            "full_name",
            "is_active",
        )
        read_only_fields = ["full_name", "level"]


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
    scope = serializers.ResourceRelatedField(
        queryset=Scope.objects.all(), required=False, many=False
    )
    included_serializers = {
        "user": UserSerializer,
        "scope": ScopeSerializer,
        "role": RoleSerializer,
    }

    class Meta:
        model = ACL
        fields = "__all__"
