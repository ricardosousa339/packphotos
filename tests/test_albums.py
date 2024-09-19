from http import HTTPStatus
import io

from fastapi.testclient import TestClient


def test_add_photo_to_album(client: TestClient, token: str):
    # Simular um arquivo de imagem
    file_content = io.BytesIO(b"fake image data")
    files = {'photo': ('test_photo.jpg', file_content, 'image/jpeg')}
    
    response = client.post(
        '/albums/2/photos',
        headers={'Authorization': f'Bearer {token}'},
        files=files,
    )
        
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response['id'] == 1
    assert json_response['album_id'] == 1
    assert json_response['name'] == 'test_photo.jpg'
    assert 'url' in json_response
    assert json_response['url'].startswith('https://')


def test_read_photos_from_album(client: TestClient):
    response = client.get('/albums/1/photos')
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert isinstance(json_response, list)
    assert len(json_response) > 0
    assert json_response[0]['id'] == 1
    assert json_response[0]['album_id'] == 1
    assert 'url' in json_response[0]
    assert json_response[0]['url'].startswith('https://')


def test_delete_photo_from_album(client, token):
    response = client.delete(
        '/albums/1/photos/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_album(client, token):
    response = client.delete(
        '/albums/1',
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
        'id': 4,
        'title': 'Test album',
    }


def test_read_albums_pagination(client):
    response = client.get('/albums/?skip=0&limit=100')
    assert response.status_code == HTTPStatus.OK
    assert 'albums' in response.json()
