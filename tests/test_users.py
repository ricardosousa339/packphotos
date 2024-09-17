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
        '/users/',
        json={
            'username': 'alice2',
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


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'email': 'teste0@test.com',
                'id': 1,
                'username': 'teste0',
            },
            {
                'email': 'blabla@hotmail.com',
                'id': 2,
                'username': 'alice',
            },
            {
                'email': 'alice@hotmail.com',
                'id': 3,
                'username': 'alice2',
            },
        ],
    }


def test_update_user_with_wrong_user(client, user, other_token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {other_token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user(client, other_user, other_token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {other_token}'},
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
        'id': other_user.id,
    }


def test_delete_user(client, user, token):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'email': 'teste0@test.com',
                'id': 1,
                'username': 'teste0',
            },
            {
                'email': 'blabla@hotmail.com',
                'id': 2,
                'username': 'alice',
            },
            {
                'email': 'alice@hotmail.com',
                'id': 3,
                'username': 'alice2',
            },
            {
                'email': 'bob@example.com',
                'id': 4,
                'username': 'bob',
            },
        ],
    }
    # assert response.json() == {'user': user.username}

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'luana',
            'email': 'luana@email.com',
            'password': '123456',
        },
    )

    print(response.json())

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'luana',
        'email': 'luana@email.com',
        'id': 5,
    }


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
