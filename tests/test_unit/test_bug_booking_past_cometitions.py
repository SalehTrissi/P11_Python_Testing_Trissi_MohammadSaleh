import pytest
# Replace with the correct way to import your Flask app
from server import app
from datetime import datetime, timedelta


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_booking_past_competition(client):
    # Example data for a past competition and a club
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Simulate going to the booking page for a past competition
    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200

    # Check if the correct error message is flashed
    if b'This competition has already taken place.' in response.data:
        assert b'Great-booking complete!' not in response.data
    else:
        # If no error message, proceed to attempt booking
        response = client.post('/purchasePlaces', data={
            'competition': competition_name,
            'club': club_name,
            'places': 3
        }, follow_redirects=True)

        assert response.status_code == 200

        # Check that an error message is flashed instead of a success message
        assert b'Great-booking complete!' not in response.data
        assert b'This competition has already taken place.' in response.data
