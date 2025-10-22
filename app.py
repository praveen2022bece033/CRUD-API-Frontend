import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 


db = SQLAlchemy(app)



class Task(db.Model):
    """Represents a task in the database."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comment', backref='task', cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "title": self.title}

class Comment(db.Model):
    """Represents a comment associated with a task."""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "task_id": self.task_id
        }


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Creates a new task."""
    data = request.get_json()
    if not data or not 'title' in data:
        return jsonify({'error': 'Title is required'}), 400
    
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({'message': 'Task created!', 'task': new_task.to_dict()}), 201



@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """(UPDATE) Edits an existing task."""
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    if not data or not 'title' in data:
        return jsonify({'error': 'Title is required'}), 400

    task.title = data['title']
    db.session.commit()

    return jsonify({'message': 'Task updated!', 'task': task.to_dict()})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """(DELETE) Deletes a specific task."""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully!'})



@app.route('/api/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment_to_task(task_id):
    """(CREATE) Adds a new comment to a specific task."""
    task = Task.query.get_or_404(task_id) 
    data = request.get_json()

    if not data or not 'text' in data:
        return jsonify({'error': 'Comment text is required'}), 400

    new_comment = Comment(text=data['text'], task_id=task.id)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'message': 'Comment added successfully!', 'comment': new_comment.to_dict()}), 201

@app.route('/api/tasks/<int:task_id>/comments', methods=['GET'])
def get_comments_for_task(task_id):
    """(READ) Gets all comments for a specific task."""
    task = Task.query.get_or_404(task_id)
    comments = [comment.to_dict() for comment in task.comments]
    return jsonify({'comments': comments})

@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id):
    """(UPDATE) Edits an existing comment."""
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()

    if not data or not 'text' in data:
        return jsonify({'error': 'Comment text is required'}), 400

    comment.text = data['text']
    db.session.commit()

    return jsonify({'message': 'Comment updated successfully!', 'comment': comment.to_dict()})

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """(DELETE) Deletes a specific comment."""
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()

    return jsonify({'message': 'Comment deleted successfully!'})



if __name__ == '__main__':

    with app.app_context():

        db.create_all()
        if not Task.query.first():
            print("Creating a sample task...")
            sample_task = Task(title="My First Sample Task")
            db.session.add(sample_task)
            db.session.commit()
            print("Sample task created with ID 1.")
    app.run(debug=True)