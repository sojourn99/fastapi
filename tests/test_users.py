from app import schemas
from jose import jwt
from app.config import settings
import pytest


def test_root(client):
    res = client.get("/")
    # print(res.json().get("message"))
    assert res.json().get("message") == "Hello World! Pushing out to Ubuntu from Github Actions."
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello1232@gmail.com", "password": "password123"})
    # print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello1232@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code, detail", [
    ('wrongemail@gmail.com', 'password123', 403, "Invalid Credentials"),
    ('sanjeev@gmail.com', 'wrongpassword', 403, "Invalid Credentials"),
    ('wrongemail@gmail.com', 'wrongpassword', 403, "Invalid Credentials"),
    (None, 'password123', 422, [{'loc': ['body', 'username'], 'msg': 'field required', 'type': 'value_error.missing'}]),
    ('sanjeev@gmail.com', None, 422, [{'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}])
])
def test_incorrect_login(test_user, client, email, password, status_code, detail):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    assert res.json().get("detail") == detail
