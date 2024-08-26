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
