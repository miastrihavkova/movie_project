from flask import Flask, request, jsonify, Response
import sqlite3
import json
import os
from typing import Union

app = Flask(__name__)

# function to set up the database if database not found or deleted
def setting_up_database() -> None:
    connection = sqlite3.connect('movie_database.db')
    connection.execute('''CREATE TABLE IF NOT EXISTS movies
    (id INTEGER, title TEXT, description TEXT, release_year INTEGER)''')
    connection.commit()

# helping function to quickly display movie from database as json
def convert_json(id: int) -> Union[Response, tuple[Response, int]]:
    connection = sqlite3.connect('movie_database.db')
    cursor = connection.cursor()
    query = "SELECT * FROM movies WHERE id = ?"
    data = cursor.execute(query, (id,)).fetchone()
    connection.commit()

    # if not found, returning error message
    if data is None:
        return jsonify({'error': 'movie not found'}), 404

    return jsonify(data)

# main page greeting
@app.route('/')
def greeting() -> str:
    setting_up_database()
    return 'welcome to movie database'

# getting all movies using sqlite3 command SELECT *
@app.route('/movies', methods=['GET'])
def get_movies() -> Response:
    setting_up_database()
    connection = sqlite3.connect('movie_database.db')
    cursor = connection.cursor()
    query = "SELECT * FROM movies"
    data = cursor.execute(query).fetchall()
    connection.commit()

    return jsonify(data)

# getting movie by id, using convert_json to display
@app.route('/movies/<int:id>', methods=['GET'])
def get_single_movie(id: int) -> Union[Response, tuple[Response, int]]:
    setting_up_database()
    return convert_json(id)

# adding one movie to the database
@app.route('/movies', methods=['POST'])
def add_movie() -> Union[Response, tuple[Response, int]]:
    setting_up_database()
    data = request.get_json()

    # checking for the existence of title and release_year data
    if not data['title'] or not data['release_year']:
        return jsonify({'error': 'missing title or release_year'}), 400

    connection = sqlite3.connect('movie_database.db')
    cursor = connection.cursor()

    # getting new unique id using the current highest id
    cursor.execute("SELECT max(id) FROM movies")
    max_id = cursor.fetchone()
    if max_id[0] is not None:
        new_id = max_id[0] + 1
    else:
        new_id = 1

    query = '''INSERT INTO MOVIES VALUES(?, ?, ?, ?)'''
    cursor.execute(query, (new_id, data['title'], data.get('description'), data['release_year']))
    connection.commit()

    return convert_json(new_id)

# updating movie by id
@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id: int) -> Union[Response, tuple[Response, int]]:
    setting_up_database()
    data = request.get_json()
    connection = sqlite3.connect('movie_database.db')
    cursor = connection.cursor()
    query = ''' UPDATE movies SET id = ?, title = ?, description = ?,
            release_year = ? WHERE id = ? '''
    cursor.execute(query, (id, data['title'], data.get('description'), data['release_year'], id))
    connection.commit()

    # checking for the changes, error in case of id not present
    if cursor.rowcount > 0:
        return convert_json(id)

    return jsonify({'error': 'update failed'}), 404

if __name__ == '__main__':
    app.run()
