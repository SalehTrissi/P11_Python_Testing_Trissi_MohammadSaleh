import pytest
from server import app, competitions, clubs

# Define a fixture to set up the Flask app for testing


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_points_deduction(client):
    # Get the initial points balance of the club
    club = next(
        (club for club in clubs if club['name'] == 'Simply Lift'), None)
    if not club:
        pytest.fail("Test club not found.")

    initial_points = int(club['points'])

    # Simulate a POST request to purchase places in a competition
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '3'  # Number of places to book
    })

    # Check if the response contains the "Great-booking complete!" flash message
    assert b'Great-booking complete!' in response.data

    # Re-fetch the club to get updated points
    updated_club = next(
        (club for club in clubs if club['name'] == 'Simply Lift'), None)
    updated_points = int(updated_club['points'])

    # Check if the points were deducted correctly from the club's balance
    assert updated_points == initial_points - \
        3, f"Expected {initial_points - 3} points, found {updated_points}"

    # Check if the competition's available places were updated correctly
    competition = next(
        (comp for comp in competitions if comp['name'] == 'Spring Festival'), None)
    assert competition is not None
    # 25 places - 3 places booked
    assert int(competition['numberOfPlaces']) == 22
