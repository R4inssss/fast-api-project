from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import schemas
from app import models
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
import pytest

# ========================= Access DB ========================== #

SQLALCHEMY_DATABASE_URL = (f'postgresql://{settings.database_username}:{settings.database_password}'
                           f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ============= Unauthed Client | Session Fixture ================ #

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# ======================= Test user fixture ======================= #

@pytest.fixture
def test_user(client):
    user_data = {"email": "test123@example.com", "password": "password123", "phone_number": ""}
    res = client.post("/users/create", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "test1234@example.com", "password": "password123", "phone_number": ""}
    res = client.post("/users/create", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})



# ======================= Client Authorization ======================= #

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


# ======================= Pytest post Fixture ======================= #

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{"title": "1st title",
                   "content": "1st content",
                   "owner_id": test_user['id']
                   },
                   {"title": "2nd title",
                   "content": "2nd content",
                   "owner_id": test_user['id']
                   },
                   {"title": "3rd title",
                   "content": "3rd content",
                   "owner_id": test_user['id']
                   },
                   {"title": "4th title",
                   "content": "4th content",
                   "owner_id": test_user2['id']
                   }]
    def create_post_model(post):
        return models.Post(**post)
    
    posts = list(map(create_post_model, posts_data))

    session.add_all(posts)

    session.commit()

    posts = session.query(models.Post).all()
    return posts

