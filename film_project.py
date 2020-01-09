#! /usr/bin/python2.7
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Genre, Film
from flask import session as login_session
import random
import string

# IMPORTS FOR GConnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

APPLICATION_NAME = "Film Catalog Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///films.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # RENDER THE LOGIN TEMPLATE
    return render_template('login.html', STATE=state)

# GConnect page
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        print "Current user is already connected."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the credentials in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    #Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']


# see if user exists: if it doesn't, make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions

def createUser(login_session):
    newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id

def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

# DISCONNECT - Revoke a current user's token and reset their login_session.
@app.route('/gdisconnect')
def gdisconnect():
    #Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

#JSON APIs to view Information of all genres & films
@app.route('/JSON')
def catalogueJSON():
    genres = session.query(Genre).all()
    films = session.query(Film).all()
    return jsonify(genres= [g.serialize for g in genres], films =[f.serialize for f in films])

#JSON APIs to view Genre Information of all Genres
@app.route('/genre/JSON')
def genresJSON():
    genres = session.query(Genre).all()
    return jsonify(genres= [g.serialize for g in genres])

#JSON APIs to view Genre Information of a specific one and its respective films
@app.route('/genre/<int:genre_id>/JSON')
def filmGenreJSON(genre_id):
    genre = session.query(Genre).filter_by(id = genre_id).one()
    films = session.query(Film).filter_by(genre_id = genre_id).all()
    return jsonify(genre = genre.serialize, films=[f.serialize for f in films])

#JSON APIs to view Film Information
@app.route('/genre/<int:genre_id>/film/<int:film_id>/JSON')
def FilmJSON(genre_id, film_id):
    Film_ID = session.query(Film).filter_by(id = film_id).one()
    return jsonify(Film_ID = Film_ID.serialize)

#Show all film genres
@app.route('/')
@app.route('/genre/')
def showGenres():
    genres = session.query(Genre).order_by(asc(Genre.name))
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    if 'username' not in login_session:
        return render_template('publicgenremenu.html', genres = genres, STATE = state)
    else:
        return render_template('genremenu.html', genres = genres, STATE = state)

#Create a new film genre
@app.route('/genre/new/', methods=['GET','POST'])
def newGenre():
  if 'username' not in login_session:
      return redirect('/login')
  if request.method == 'POST':
      newGenre = Genre(name = request.form['name'], user_id = login_session['user_id'])
      session.add(newGenre)
      flash('New Genre %s Successfully Created' % newGenre.name)
      session.commit()
      return redirect(url_for('showGenres'))
  else:
      return render_template('newgenre.html')

#Edit a film genre
@app.route('/genre/<int:genre_id>/edit/', methods = ['GET', 'POST'])
def editGenre(genre_id):
  genreToEdit = session.query(Genre).filter_by(id = genre_id).one()
  if 'username' not in login_session:
      return redirect('/login')
  if genreToEdit.user_id != login_session['user_id']:
      return "<script>function myFunction() {alert('You are not authorized to edit this film genre. Please create your own film genre in order to edit.');}</script><body onload = 'myFunction()''>"
  if request.method == 'POST':
      if request.form['name']:
        genreToEdit.name = request.form['name']
        flash('Genre Successfully Edited %s' % genreToEdit.name)
        return redirect(url_for('showGenres'))
  else:
    return render_template('editgenre.html', genre = genreToEdit)


#Delete a film genre
@app.route('/genre/<int:genre_id>/delete/', methods = ['GET','POST'])
def deleteGenre(genre_id):
  genreToDelete = session.query(Genre).filter_by(id = genre_id).one()
  if 'username' not in login_session:
      return redirect('/login')
  if genreToDelete.user_id != login_session['user_id']:
      return "<script>function myFunction() {alert('You are not authorized to delete this genre. Please create your own genre in order to delete.');}</script><body onload = 'myFunction()''>"
  if request.method == 'POST':
    session.delete(genreToDelete)
    flash('%s Successfully Deleted' % genreToDelete.name)
    session.commit()
    return redirect(url_for('showGenres', genre_id = genre_id))
  else:
    return render_template('deletegenre.html',genre = genreToDelete)

#Show a film genre listing
@app.route('/genre/<int:genre_id>/')
@app.route('/genre/<int:genre_id>/film/')
def showFilms(genre_id):
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    genre = session.query(Genre).filter_by(id = genre_id).one()
    creator = getUserInfo(genre.user_id)
    films = session.query(Film).filter_by(genre_id = genre_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicfilmmenu.html', films = films, genre = genre, creator = creator, STATE = state)
    else:
        return render_template('filmmenu.html', films = films, genre = genre, creator = creator, STATE = state)



#Create a new film
@app.route('/genre/<int:genre_id>/film/new/',methods=['GET','POST'])
def newFilm(genre_id):
  genre = session.query(Genre).filter_by(id = genre_id).one()
  if 'username' not in login_session:
      return redirect('/login')
  if genre.user_id != login_session['user_id']:
      return "<script>function myFunction() {alert('You are not authorized to add films to this genre. Please create your own genre in order to add films.');}</script><body onload = 'myFunction()''>"
  if request.method == 'POST':
      newFilm = Film(title = request.form['title'], year = request.form['year'], description = request.form['description'], poster_image = request.form['poster_image'], genre_id = genre_id, user_id = login_session['user_id'])
      session.add(newFilm)
      flash('New Film %s Successfully Created' % (newFilm.title))
      session.commit()
      return redirect(url_for('showFilms', genre_id = genre_id))
  else:
      return render_template('newfilm.html', genre_id = genre_id)

#Edit a film
@app.route('/genre/<int:genre_id>/film/<int:film_id>/edit', methods=['GET','POST'])
def editFilm(genre_id, film_id):
    filmToEdit = session.query(Film).filter_by(id = film_id).one()
    genre = session.query(Genre).filter_by(id = genre_id).one()
    if 'username' not in login_session:
         return redirect('/login')
    if genre.user_id != login_session['user_id']:
      return "<script>function myFunction() {alert('You are not authorized to edit films of this genre. Please create your own genre in order to edit films.');}</script><body onload = 'myFunction()''>"
    if request.method == 'POST':
        if request.form['title']:
            filmToEdit.title = request.form['title']
        if request.form['description']:
            filmToEdit.description = request.form['description']
        if request.form['year']:
            filmToEdit.year = request.form['year']
        if request.form['poster_image']:
            filmToEdit.poster_image = request.form['poster_image']
        session.add(filmToEdit)
        flash('Film Successfully Edited')
        session.commit()
        return redirect(url_for('showFilms', genre_id = genre_id))
    else:
        return render_template('editfilm.html', genre_id = genre_id, film_id = film_id, film = filmToEdit)


#Delete a film
@app.route('/genre/<int:genre_id>/film/<int:film_id>/delete', methods = ['GET','POST'])
def deleteFilm(genre_id, film_id):
    genre = session.query(Genre).filter_by(id = genre_id).one()
    filmToDelete = session.query(Film).filter_by(id = film_id).one()
    if 'username' not in login_session:
      return redirect('/login')
    if genre.user_id != login_session['user_id']:
      return "<script>function myFunction() {alert('You are not authorized to delete films of this genre. Please create your own genre in order to delete films.');}</script><body onload = 'myFunction()''>"
    if request.method == 'POST':
        session.delete(filmToDelete)
        session.commit()
        flash('Film Successfully Deleted')
        return redirect(url_for('showFilms', genre_id = genre_id))
    else:
        return render_template('deletefilm.html', film = filmToDelete)


if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)
