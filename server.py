from datetime import datetime
import json
from flask import Flask, render_template, request, redirect, flash, url_for, session


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


@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    if request.method == 'POST':
        email = request.form['email']
        club = next((club for club in clubs if club['email'] == email), None)

        if club is not None:
            session['club'] = club  # Store the club data in the session
            return render_template('welcome.html', club=club, competitions=competitions)
        else:
            flash("Invalid email. Please try again.")
            return redirect(url_for('index'))
    else:
        # Check if 'club' is in the session and retrieve it
        if 'club' in session:
            club = session['club']
            return render_template('welcome.html', club=club, competitions=competitions)
        else:
            flash("Please enter your email to access the summary.")
            return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    # Convert competition date to a datetime object
    competition_date = datetime.strptime(
        foundCompetition['date'], '%Y-%m-%d %H:%M:%S')

    # Check if the competition date is in the past
    if datetime.now() > competition_date:
        flash('This competition has already taken place.', 'error')
        return render_template('welcome.html', club=foundClub, competitions=competitions)

    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=foundClub, competitions=competitions)


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
        return render_template('welcome.html', club=club, competitions=competitions)

    # Check if the club has already booked places for this competition
    places_already_booked = club['places_booked'].get(competition_name, 0)

    # Calculate the total places booked, including the new booking
    total_places_booked = places_already_booked + placesRequired

    if total_places_booked > 12:
        flash('You can book no more than 12 places in each competition.')
        return redirect(url_for('book', competition=competition_name, club=club_name))

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

    # Update the places_booked record for the club
    club['places_booked'][competition_name] = total_places_booked

    # Display a success message
    flash('Great-booking complete!', 'success')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
