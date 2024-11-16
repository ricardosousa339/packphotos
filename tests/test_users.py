from http import HTTPStatus


def test_create_existing_username(client):
    client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'blabla@hotmail.com',
            'password': 'secret123',
        },
    )

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@gmail.com',
            'password': 'secret123',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_existing_email(client):
    response = client.post(
    response = client.post(
        '/users/',
        json={
            'username': 'alessandra',
            'email': 'alice@hotmail.com',
            'password': 'secret123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        '/users/',
        json={
            'username': 'aliceandra',
            'email': 'alice@hotmail.com',
            'password': 'secret123',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client, user):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    users = response.json()
    assert len(users) > 0
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    users = response_data.get('users', [])

    for user_ in users:
        assert 'id' in user_
        assert 'username' in user_
        assert 'email' in user_
        assert '@' in user_['email']
        assert '.' in user_['email'].split('@')[1]


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    response_data = response.json()

    assert user_schema in response_data['users']


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user(client, user, token):
    print(f'User updted: {user}')
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    print(response)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'marli',
            'email': 'marli@example.com',
            'password': 'secreto',
        },
    )

    print(response.json())

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'marli',
        'email': 'marli@example.com',
        'id': 5,
    }


def test_delete_user(client, other_user, other_token):
    print(other_token)
    print(f'User: {other_user}')
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {other_token}'},
    )

    print(f'Response status code: {response.status_code}')
    print(f'Response body: {response.json()}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
