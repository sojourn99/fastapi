from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Dependency
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)


def test_root():
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World! Pushing out to Ubuntu. Another change."
    assert res.status_code == 200


def test_create_user():
    res = client.post("/users/", json={"email": "hello1232@gmail.com", "password": "password123"})
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello1232@gmail.com"
    assert res.status_code == 201
