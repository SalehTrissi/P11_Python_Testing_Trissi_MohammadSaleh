import pytest
from server import app, competitions, clubs


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_redeem_points_negative_balance(client):
    # Choose a club and competition for the test
    club_name = "Simply Lift"
    competition_name = "Spring Festival"
    club = next((c for c in clubs if c['name'] == club_name), None)
    competition = next(
        (c for c in competitions if c['name'] == competition_name), None)

    # Calculate available points (e.g., 13 points for "Simply Lift")
    available_points = int(club['points'])

    # Attempt to redeem more points than available
    places_to_redeem = available_points + 1  # Attempt to go into negative balance
    data = {
        'competition': competition_name,
        'club': club_name,
        'places': places_to_redeem
    }

    # Perform the purchasePlaces POST request
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)

    # Check if the response contains the "Not enough points to redeem" flash message
    assert b'Not enough points to redeem.' in response.data

    # Check if the club's points balance remains the same
    assert int(club['points']) == available_points
