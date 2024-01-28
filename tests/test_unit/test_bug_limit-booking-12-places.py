import pytest
from bs4 import BeautifulSoup
from server import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    with app.test_client() as client:
        yield client


@pytest.fixture
def clubs():
    return loadClubs()


@pytest.fixture
def competitions():
    return loadCompetitions()


def test_bug_limit_booking_12_places(client, clubs, competitions):
    """
    As a club, I should not be able to book more than 12 places for a single competition.
    """
    club_name = "Simply Lift"
    competition_name = "Spring Festival"
    club = next((c for c in clubs if c['name'] == club_name), None)
    competition = next(
        (c for c in competitions if c['name'] == competition_name), None)

    if not club or not competition:
        pytest.fail(f'Required club or competition not found for the test.')

    # Try booking 13 places, which is more than the allowed limit
    places_to_book = 13
    data = {
        'competition': competition_name,
        'club': club_name,
        'places': places_to_book
    }

    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    soup = BeautifulSoup(response.data, 'html.parser')

    # Parse HTML response to find the alert message
    alert_text = soup.find('div', class_='alert').get_text(
        strip=True) if soup.find('div', class_='alert') else ''

    # Assert that the expected error message is present
    assert 'You can book no more than 12 places in each competition.' in alert_text, "Error message for booking more than 12 places not found."

    # Assert that the club's points and competition places are unchanged
    updated_club = next((c for c in clubs if c['name'] == club_name), None)
    updated_competition = next(
        (c for c in competitions if c['name'] == competition_name), None)
    assert updated_club['points'] == club['points'], "Club points should not have changed"
    assert updated_competition['numberOfPlaces'] == competition['numberOfPlaces'], "Competition places should not have changed"
