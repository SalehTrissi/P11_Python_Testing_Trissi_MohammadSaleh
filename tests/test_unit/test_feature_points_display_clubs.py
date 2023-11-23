import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_secretary_can_see_club_points_list(client):
    # Simulate a login process (you may need to adjust this depending on your authentication logic)
    response = client.post('/showSummary', data={
        'email': 'john@simplylift.co'
    })

    # Check that the login was successful
    assert response.status_code == 200

    # Now, make a request to the Club Points List page
    response = client.get('/clubPointsList')

    # Check that the Club Points List page is accessible and contains club names and points
    assert response.status_code == 200
    assert b"Club Points List" in response.data
    assert b"Club Name" in response.data
    assert b"Points Available" in response.data

    # Check for a specific club nam
    assert b"Simply Lift" in response.data

    # Check for the points of the specific club
    assert b"13" in response.data
