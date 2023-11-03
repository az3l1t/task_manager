from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Исправлено неправильное использование имени аргумента

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    status = db.Column(db.String(20), default='todo')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    result = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status
        }
        result.append(task_data)
    return jsonify(result)

@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json.get('description', '')
    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created with code 0'})

@app.route('/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'})
    
    if request.method == 'GET':
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status
        }
        return jsonify(task_data)
    
    elif request.method == 'PUT':
        title = request.json.get('title', task.title)
        description = request.json.get('description', task.description)
        status = request.json.get('status', task.status)
        task.title = title
        task.description = description
        task.status = status
        db.session.commit()  # Добавлен коммит
        return jsonify({'message': 'Task updated'})
    
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted with code 0'})

if __name__ == '__main__':
    app.run(host='localhost', port=5000)  # Исправлено значение host