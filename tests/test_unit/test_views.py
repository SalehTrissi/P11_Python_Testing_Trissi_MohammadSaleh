import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_show_summary_with_login(client):
    with client.session_transaction() as sess:
        sess['club'] = {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        }
    response = client.get('/showSummary')
    assert response.status_code == 200


def test_show_summary_without_login(client):
    response = client.get('/showSummary')
    assert response.status_code == 302


def test_book_nonexistent_entities(client):
    response = client.get('/book/NonexistentCompetition/NonexistentClub')
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data


def test_purchase_places_for_nonexistent_entities(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'NonexistentCompetition',
        'club': 'NonexistentClub',
        'places': 3
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid competition or club.' in response.data


def test_book_with_existing_bookings(client):
    # Assuming 'Test Club' has booked places for 'Test Competition' in your test data
    response = client.get("/book/Testing%20Date/Simply%20Lift")
    assert response.status_code == 200
