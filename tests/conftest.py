from fastapi.testclient import TestClient

from app import models
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
import pytest

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    # drop all tables
    Base.metadata.drop_all(bind=engine)
    # create database tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db
    # run code before running test
    yield TestClient(app)
    # run code after test finishes


@pytest.fixture
def test_user(client):
    user_data = {"email": "someuser@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "sanjeev123@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
        },
        {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
        }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']),
    #                 models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
