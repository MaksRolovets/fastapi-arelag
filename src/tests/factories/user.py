from uuid import uuid4

from schemas.user import RequestUserModel


def user_factory(email: str | None = None):
    return RequestUserModel(
        email=email or f"{uuid4().hex}@test.com"
    )