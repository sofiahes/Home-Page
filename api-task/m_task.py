from flask import Flask,jsonify, request, abort
app = Flask(__name__)
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid

#base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@database-p.cgyaycco1nat.us-east-1.rds.amazonaws.com:5432/postgres'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

@app.route('/test3', methods=['GET'])
def test1():
    return 'FUNCIONA EL TASK!'

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.String(36), nullable=False,
                   default=lambda: str(uuid.uuid4()), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    done = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Task {self.title}>"

    def __init__(self, title, description, done):
        self.title = title
        self.description = description
        self.done = done

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done
        }

CORS(app, resources={r'/*': {'origins': '*'}})

def remove_task(task_id):
    _task = Task.query.filter_by(id=task_id).first()
    db.session.delete(_task)
    db.session.commit()
    return _task

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/tasks', methods=['GET', 'POST'])
def all_tasks():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        task = Task(title=post_data.get('title'), description=post_data.get('description'), done=post_data.get('done'))
        db.session.add(task)
        db.session.commit()
        response_object['message'] = 'Task added!'
    else:
        response_object['tasks'] = [task.serialize() for task in Task.query.all()]
    return jsonify(response_object)

@app.route('/tasks/<task_id>', methods=['PUT', 'DELETE'])
def single_task(task_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_task(task_id)
        task = Task(title=post_data.get('title'), description=post_data.get('description'), done=post_data.get('done'))
        db.session.add(task)
        db.session.commit()
        response_object['message'] = 'Task updated!'
    if request.method == 'DELETE':
        remove_task(task_id)
        response_object['message'] = 'Task removed!'
    return jsonify(response_object)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
