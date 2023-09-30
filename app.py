from flask import Flask,jsonify, request, abort
app = Flask(__name__)
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@database-p.cgyaycco1nat.us-east-1.rds.amazonaws.com:5432/postgres'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


# import declared routes
import m_peliculas
import m_task
import m_books

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
