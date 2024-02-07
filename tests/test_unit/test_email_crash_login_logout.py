from bs4 import BeautifulSoup
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

    response = client.get(response.location)

    # Decode the response data from bytes to a string
    response_data = response.data.decode('utf-8')

    # Parse the HTML
    soup = BeautifulSoup(response_data, 'html.parser')

    # Find div with class alert and get its text content
    alert_text = soup.find('div', class_='alert').get_text(strip=True)

    # Assert that the message "Invalid email. Please try again." is in the alert text
    assert "Invalid email. Please try again." in alert_text


def test_login(client):
    # Test login by posting a valid email
    response = client.post('/showSummary', data={
        'email': 'john@simplylift.co',
    }, follow_redirects=True)

    # Assert that the response contains the expected content
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_logout(client):
    # Test logout by visiting the /logout route
    response = client.get('/logout', follow_redirects=True)

    # Assert that the response redirects to the index page
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
