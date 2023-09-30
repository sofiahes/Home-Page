from __main__ import app,db
import uuid
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

@app.route('/prueba2', methods=['GET'])
def test2():
    return 'FUNCIONA LA PELI!'

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    director = db.Column(db.String(80))
    year = db.Column(db.Integer)
    watched = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Movie {self.title}>"

    def __init__(self, title, director, year, watched):
        self.title = title
        self.director = director
        self.year = year
        self.watched = watched

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'director': self.director,
            'year': self.year,
            'watched': self.watched
        }

def remove_movie(movie_id):
    _movie = Movie.query.filter_by(id=movie_id).first()
    db.session.delete(_movie)
    db.session.commit()
    return _movie

@app.route('/movies', methods=['GET', 'POST'])
def all_movies():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        movie = Movie(title=post_data.get('title'), director=post_data.get('director'), year=post_data.get('year'), watched=post_data.get('watched'))
        db.session.add(movie)
        db.session.commit()
        response_object['message'] = 'Movie added!'
    else:
        response_object['movies'] = [movie.serialize() for movie in Movie.query.all()]
    return jsonify(response_object)


@app.route('/movies/<movie_id>', methods=['PUT', 'DELETE'])
def single_movie(movie_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_movie(movie_id)
        movie = Movie(title=post_data.get('title'), director=post_data.get('director'), year=post_data.get('year'), watched=post_data.get('watched'))
        db.session.add(movie)
        db.session.commit()
        response_object['message'] = 'Movie updated!'
    if request.method == 'DELETE':
        remove_movie(movie_id)
        response_object['message'] = 'Movie removed!'
    return jsonify(response_object)