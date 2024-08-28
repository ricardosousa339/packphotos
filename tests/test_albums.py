from http import HTTPStatus

import pytest


def test_create_albums(client, token):
    response = client.post(
        '/albums/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test album',
        },
    )
    assert response.json() == {
        'id': 1,
        'title': 'Test album',
    }


@pytest.mark.usefixtures('_create_albums')
def test_read_albums(client):
    response = client.get('/albums/')
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert 'albums' in json_response
    assert isinstance(json_response['albums'], list)


@pytest.mark.usefixtures('_create_albums')
def test_update_album(client, token):
    response = client.put(
        '/albums/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Updated album',
        },
    )

    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response['id'] == 1
    assert json_response['title'] == 'Updated album'


def test_add_photo_to_album(client, token):
    response = client.post(
        '/albums/1/photos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Photo 1',
            'url': 'https://example.com/photo.jpg',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'album_id': 1,
        'url': 'https://example.com/photo.jpg',
        'name': 'Photo 1',
    }


def test_delete_album(client, token):
    response = client.delete(
        '/albums/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.usefixtures('_create_albums')
def test_read_album(client):
    response = client.get('/albums/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'title': 'Test album 1',
    }


def test_delete_photo_from_album(client, token):
    response = client.delete(
        '/albums/1/photos/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_create_album(client, token):
    response = client.post(
        '/albums/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test album',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'title': 'Test album',
    }


def test_read_albums_pagination(client):
    response = client.get('/albums/?skip=0&limit=100')
    assert response.status_code == HTTPStatus.OK
    assert 'albums' in response.json()


def test_read_photos_from_album(client):
    response = client.get('/albums/1/photos')
    assert response.status_code == HTTPStatus.OK
    assert 'photos' in response.json()
