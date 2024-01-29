import pytest
from server import app as flask_app


@pytest.fixture
def app():
    app = flask_app
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_show_summary(client):
    response = client.post(
        '/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200


def test_book(client):
    response = client.get('/book/Testing%20Date/Simply%20Lift')
    assert response.status_code == 200


def test_purchase_places(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Testing Date',
        'club': 'john@simplylift.co',
        'places': 5
    })
    assert response.status_code == 200


def test_club_points_list(client):
    response = client.get('/clubPointsList')
    assert response.status_code == 200
