import pytest
from server import app, competitions, clubs


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_points_deduction(client):
    # Get the initial points balance of the club
    initial_points = int(clubs[0]['points'])

    # Simulate a POST request to purchase places in a competition
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '3'  # Number of places to book
    })

    # Check if the response contains the "Great - booking complete!" flash message
    assert b'Great - booking complete!' in response.data

    # Check if the points were deducted correctly from the club's balance
    updated_points = int(clubs[0]['points'])
    assert updated_points == initial_points - 3 == 10  # 13 points - 3 points used

    # Check if the competition's available places were updated correctly
    competition = next(
        (comp for comp in competitions if comp['name'] == 'Spring Festival'), None)

    assert competition is not None
    # 25 places - 3 places booked
    assert int(competition['numberOfPlaces']) == 22

    # Simulate a POST request with insufficient points
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '15'  # Assuming the club has fewer than 15 points
    })

    # Check if the response contains the "Insufficient points to make the booking." flash message
    assert b'Insufficient points to make the booking.' in response.data
