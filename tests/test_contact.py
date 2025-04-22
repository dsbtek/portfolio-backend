def test_get_contact_info(client, sample_contact):
    response = client.get('/api/contact/')
    assert response.status_code == 200
    assert response.json['email'] == 'test@example.com'
    assert response.json['linkedin'] == 'https://linkedin.com/in/test'


def test_submit_contact_form(client):
    response = client.post('/api/contact/message/',
                           json={
                               'name': 'Test User',
                               'email': 'test@example.com',
                               'message': 'Test message'
                           }
                           )
    assert response.status_code == 201


def test_update_contact_info(client, auth_headers):
    response = client.post('/api/contact/',
                           headers=auth_headers,
                           json={
                               'email': 'contact@example.com',
                               'linkedin': 'https://linkedin.com/in/test',
                               'github': 'https://github.com/test',
                               'twitter': 'https://twitter.com/test'
                           }
                           )
    assert response.status_code == 200
