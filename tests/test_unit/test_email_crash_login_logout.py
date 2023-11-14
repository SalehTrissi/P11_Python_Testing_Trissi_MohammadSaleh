import pytest
from server import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client


def test_email_not_found(client):
    response = client.post('/showSummary', data={
        'email': 'nonexistent@example.com',
    })
    # Assert that the response redirects to the index page with a 302 status code
    assert response.status_code == 302
    assert response.location == "http://localhost/"

    response = client.get(response.location)
    assert b"Sorry, that email wasn't found." in response.data


def test_login(client):
    # Test login by posting a valid email
    response = client.post('/showSummary', data={
        'email': 'john@simplylift.co',
    }, follow_redirects=True)

    # Assert that the response contains the expected content
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"Great-booking complete!" not in response.data


def test_logout(client):
    # Test logout by visiting the /logout route
    response = client.get('/logout', follow_redirects=True)

    # Assert that the response redirects to the index page
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert b"Great-booking complete!" not in response.data  # Ensure no booking message
