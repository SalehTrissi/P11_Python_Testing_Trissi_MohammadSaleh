import pytest
from bs4 import BeautifulSoup
from server import app, competitions, clubs


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def get_club_and_competition():
    def _get_club_and_competition(club_name, competition_name):
        club = next((c for c in clubs if c['name'] == club_name), None)
        competition = next(
            (c for c in competitions if c['name'] == competition_name), None)
        return club, competition
    return _get_club_and_competition


def test_redeem_points_negative_balance(client, get_club_and_competition):
    club_name = "Simply Lift"
    competition_name = "Spring Festival"
    club, competition = get_club_and_competition(club_name, competition_name)

    # Set the club's points to a known value less than 12
    club['points'] = 10

    # Try to redeem more points than the club has but within the 12 places limit
    places_to_redeem = 11  # More than available points but less than 12
    data = {
        'competition': competition_name,
        'club': club_name,
        'places': places_to_redeem
    }

    response = client.post('/purchasePlaces', data=data, follow_redirects=True)

    # Parse HTML response to find the alert message
    soup = BeautifulSoup(response.data, 'html.parser')
    alert_text = soup.find('div', class_='alert').get_text(
        strip=True) if soup.find('div', class_='alert') else ''

    # Assert that the expected error message is present
    assert 'Not enough points to redeem.' in alert_text, "Error message not found in response"

    # Check if the club's points balance remains unchanged
    updated_club, _ = get_club_and_competition(
        club_name, competition_name)  # Re-fetch to get updated data
    assert int(
        updated_club['points']) == 10, "Club points should not have changed"
