import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'
app.debug = True

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = next(
            club for club in clubs if club['email'] == request.form['email'])
    except StopIteration:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    places_required = int(request.form['places'])

    # Find the selected competition and club
    competition = next(
        (c for c in competitions if c['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)

    if competition is None or club is None:
        flash('Invalid competition or club.')
        return redirect(url_for('index'))

    # Check if the club has already booked places for this competition
    if competition_name in club['places_booked']:
        places_already_booked = club['places_booked'][competition_name]
    else:
        places_already_booked = 0

    # Calculate the total places booked, including the new booking
    total_places_booked = places_already_booked + places_required

    if places_already_booked > 0 and total_places_booked > 12:
        flash('You can book no more than 12 places in each competition.')
        return redirect(url_for('book', competition=competition_name, club=club_name))

    available_places = int(competition['numberOfPlaces'])

    # Deduct the places if the request is valid
    competition['numberOfPlaces'] = str(available_places - places_required)

    # Update the places booked by the club for this competition
    club['places_booked'][competition_name] = total_places_booked

    flash('Great-booking complete!', 'success')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
