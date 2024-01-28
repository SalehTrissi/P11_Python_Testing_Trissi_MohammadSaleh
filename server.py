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
    placesRequired = int(request.form['places'])

    # Find the selected competition and club
    competition = next(
        (comp for comp in competitions if comp['name'] == competition_name), None)
    club = next((club for club in clubs if club['name'] == club_name), None)

    # Check if the competition or club is not found
    if not competition or not club:
        flash('Invalid competition or club.')
        return render_template('welcome.html', club=club, competition=competition)

    # Calculate the available points of the club
    available_points = int(club['points'])

    # Check if there are enough points to redeem
    if placesRequired > available_points:
        flash('Not enough points to redeem.')
        return render_template('booking.html', club=club, competition=competition)

    # Deduct the redeemed points from the club's total and update available places
    competition['numberOfPlaces'] = int(
        competition['numberOfPlaces']) - placesRequired
    club['points'] = available_points - placesRequired

    # Display a success message
    flash('Great-booking complete!', 'success')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
