from django.urls import reverse
from rest_framework.exceptions import ValidationError

from emeis.core.models import Scope, User
from emeis.core.validation import EmeisBaseValidator, ValidatorMixin, validator_for


def test_custom_validation(admin_client, user, reset_config_classes):
    class LowercaseUsername(EmeisBaseValidator):
        @validator_for(User)
        def lowercase_username(self, data):
            data["username"] = data["username"].lower()
            return data

    class RejectEverything(EmeisBaseValidator):
        # Two validator markers - we support stacking/chaining
        @validator_for(User)
        @validator_for(Scope)
        def reject_all(self, data):
            raise ValidationError("NOPE")

    def send_update():
        return admin_client.patch(
            url,
            data=(
                {
                    "data": {
                        "attributes": {"username": "USERNAME"},
                        "type": "users",
                        "id": str(user.pk),
                    }
                }
            ),
        )

    url = reverse("user-detail", args=[user.pk])

    # First, check if rejection works
    ValidatorMixin.register_validation_classes([RejectEverything])
    resp = send_update()
    assert resp.json()["errors"][0]["detail"] == "NOPE"

    # Then, check if the data modification works
    ValidatorMixin.register_validation_classes([LowercaseUsername])

    resp = send_update()
    assert resp.json()["data"]["attributes"]["username"] == "username"

    # Also check in DB
    user.refresh_from_db()
    assert user.username == "username"
