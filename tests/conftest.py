from http import HTTPStatus

import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import Photo, User, table_registry
from fast_zero.security import get_password_hash


@pytest.fixture(scope='session')
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
    session.close()
    table_registry.metadata.drop_all(engine)


@pytest.fixture(scope='session')
def user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture(scope='session')
def other_user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture(scope='session')
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    print(response)
    return response.json()['access_token']


@pytest.fixture(scope='session')
def other_token(client, other_user):
    response = client.post(
        '/auth/token',
        data={
            'username': other_user.email,
            'password': other_user.clean_password,
        },
    )
    print(response)
    return response.json()['access_token']


@pytest.fixture(scope='session')
def create_albums(client, token):
    client.post(
        '/albums/',
        headers={'Authorization': f'Bearer {token}'},
        json={'id': 1, 'title': 'Test album 1'},
    )
    response = client.post(
        '/albums/',
        headers={'Authorization': f'Bearer {token}'},
        json={'id': 2, 'title': 'Test album 2'},
    )

    assert response.status_code == HTTPStatus.OK
    return response.json()

    # TODO: Fazer funcionar a criacao de album no teste com id !+ None


def photo(session):
    photo = PhotoFactory()
    session.add(photo)
    session.commit()
    session.refresh(photo)
    return photo


class PhotoFactory(factory.Factory):
    class Meta:
        model = Photo

    # Define the attributes for the Photo model here
    # For example:
    title = factory.Sequence(lambda n: f'Photo {n}')
    description = factory.Faker('sentence')
    image_url = factory.Faker('image_url')


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'teste{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
