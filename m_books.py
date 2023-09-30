from __main__ import app,db
import uuid
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

@app.route('/', methods=['GET'])
def test1():
    return 'FUNCIONA!'

class Book(db.Model):   
    __tablename__ = 'books'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    read = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

    def __init__(self, title, author, read):
        self.title = title
        self.author = author
        self.read = read
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'read': self.read
        }


def remove_book(book_id):
    _book = Book.query.filter_by(id=book_id).first()
    db.session.delete(_book)
    db.session.commit()
    return _book


@app.route('/books', methods=['GET','POST'])
def all_books():
    if request.method == 'POST':
        post_data = request.get_json()
        book = Book(title=post_data.get('title'), author=post_data.get('author'), read=post_data.get('read'))
        db.session.add(book)
        db.session.commit()
        response_object = {'message': 'Book added!'}
    else:
        books = Book.query.all()
        response_object = {'books': [book.serialize() for book in books]}
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        book = Book(title=post_data.get('title'), author=post_data.get('author'), read=post_data.get('read'))
        db.session.add(book)
        db.session.commit()
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)