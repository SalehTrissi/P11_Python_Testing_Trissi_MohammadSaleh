import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_booking_page_for_past_competition_shows_error(client):
    # Example data for a past competition and a club
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Simulate going to the booking page for a past competition
    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200

    # Check if the correct error message is flashed
    assert b'This competition has already taken place.' in response.data
    assert b'Great-booking complete!' not in response.data
