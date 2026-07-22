import pytest

from brokers.dhan.authentication import AuthenticationService
from brokers.dhan.exceptions import AuthenticationError


def test_authentication_service_accepts_valid_credentials():
    service = AuthenticationService()

    assert (
        service.authenticate(
            client_id="client123",
            access_token="token123",
        )
        is True
    )


@pytest.mark.parametrize(
    "client_id,access_token",
    [
        ("", "token"),
        ("client", ""),
        ("", ""),
        (None, "token"),
        ("client", None),
        (None, None),
    ],
)
def test_authentication_rejects_invalid_credentials(
    client_id,
    access_token,
):
    service = AuthenticationService()

    with pytest.raises(AuthenticationError):
        service.authenticate(client_id, access_token)
