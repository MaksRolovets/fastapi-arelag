from http import HTTPStatus

from tests.factories.user import user_factory


async def test_create_user(client):
    user = user_factory()

    response = await client.post(
        "/users",
        json=user.model_dump(),
    )

    assert response.status_code == HTTPStatus.OK

    body = response.json()

    assert body["email"] == user.email
    assert body["status"] == "ACTIVE"
    assert "id" in body


async def test_get_users(client):
    user = user_factory()

    await client.post(
        "/users",
        json=user.model_dump(),
    )

    response = await client.get("/users")

    assert response.status_code == HTTPStatus.OK

    users = response.json()

    assert len(users) >= 1
    assert any(x["email"] == user.email for x in users)


async def test_create_existing_user(client):
    user = user_factory()

    await client.post(
        "/users",
        json=user.model_dump(),
    )

    response = await client.post(
        "/users",
        json=user.model_dump(),
    )

    assert response.status_code == HTTPStatus.CONFLICT




async def test_block_user(client):
    user = user_factory()

    response = await client.post(
        "/users",
        json=user.model_dump(),
    )

    created_user = response.json()

    response = await client.patch(
        f"/users/{created_user['id']}",
        json={
            "status": "BLOCKED",
        },
    )

    assert response.status_code == HTTPStatus.OK

    body = response.json()

    assert body["status"] == "BLOCKED"


async def test_activate_user(client):
    user = user_factory()

    response = await client.post(
        "/users",
        json=user.model_dump(),
    )

    created_user = response.json()

    await client.patch(
        f"/users/{created_user['id']}",
        json={
            "status": "BLOCKED",
        },
    )

    response = await client.patch(
        f"/users/{created_user['id']}",
        json={
            "status": "ACTIVE",
        },
    )

    assert response.status_code == HTTPStatus.OK

    body = response.json()

    assert body["status"] == "ACTIVE"


async def test_update_unknown_user(client):
    response = await client.patch(
        "/users/999999",
        json={
            "status": "BLOCKED",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_block_blocked_user(client):
    user = user_factory()

    response = await client.post(
        "/users",
        json=user.model_dump(),
    )

    created_user = response.json()

    await client.patch(
        f"/users/{created_user['id']}",
        json={
            "status": "BLOCKED",
        },
    )

    response = await client.patch(
        f"/users/{created_user['id']}",
        json={
            "status": "BLOCKED",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


async def test_activate_active_user(client):
    user = user_factory()

    response = await client.post(
        "/users",
        json=user.model_dump(),
    )

    created_user = response.json()

    response = await client.patch(
        f"/users/{created_user['id']}",
        json={
            "status": "ACTIVE",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


async def test_get_user_by_email(client):
    user = user_factory()

    await client.post(
        "/users",
        json=user.model_dump(),
    )

    response = await client.get(
        f"/users?email={user.email}",
    )

    assert response.status_code == HTTPStatus.OK

    users = response.json()

    assert len(users) == 1
    assert users[0]["email"] == user.email


async def test_get_users_by_status(client):
    user = user_factory()

    response = await client.post(
        "/users",
        json=user.model_dump(),
    )

    created_user = response.json()

    await client.patch(
        f"/users/{created_user['id']}",
        json={
            "status": "BLOCKED",
        },
    )

    response = await client.get(
        "/users?user_status=BLOCKED",
    )

    assert response.status_code == HTTPStatus.OK

    users = response.json()

    assert any(x["status"] == "BLOCKED" for x in users)