import pytest
import json
from app import app, db, Task, Comment


@pytest.fixture
def client():
   
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    

    with app.test_client() as client:

        with app.app_context():
            db.create_all()

            yield client
            db.drop_all()



def test_add_comment(client):
    """Tests the POST /api/tasks/<id>/comments endpoint."""

    with app.app_context():
        new_task = Task(title="Test Task")
        db.session.add(new_task)
        db.session.commit()
        task_id = new_task.id

    response = client.post(
        f'/api/tasks/{task_id}/comments',
        data=json.dumps({'text': 'A new test comment'}),
        content_type='application/json'
    )
    
    
    assert response.status_code == 201 
    data = response.get_json()
    assert data['message'] == 'Comment added successfully!'
    assert data['comment']['text'] == 'A new test comment'

def test_get_comments(client):
    """Tests the GET /api/tasks/<id>/comments endpoint."""

    with app.app_context():
        task = Task(title="Task with a comment")
        comment = Comment(text="You should see this comment", task=task)
        db.session.add(task)
        db.session.add(comment)
        db.session.commit()
        task_id = task.id


    response = client.get(f'/api/tasks/{task_id}/comments')

    assert response.status_code == 200
    data = response.get_json()
    assert len(data['comments']) == 1
    assert data['comments'][0]['text'] == 'You should see this comment'

def test_edit_comment(client):
    """Tests the PUT /api/comments/<id> endpoint."""

    with app.app_context():
        task = Task(title="Task")
        comment = Comment(text="Original text", task=task)
        db.session.add_all([task, comment])
        db.session.commit()
        comment_id = comment.id


    response = client.put(
        f'/api/comments/{comment_id}',
        data=json.dumps({'text': 'Updated text'}),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    assert response.get_json()['comment']['text'] == 'Updated text'

def test_delete_comment(client):
    """Tests the DELETE /api/comments/<id> endpoint."""

    with app.app_context():
        task = Task(title="Task")
        comment = Comment(text="To be deleted", task=task)
        db.session.add_all([task, comment])
        db.session.commit()
        comment_id = comment.id
        task_id = task.id


    response = client.delete(f'/api/comments/{comment_id}')

    assert response.status_code == 200
    assert response.get_json()['message'] == 'Comment deleted successfully!'

    get_response = client.get(f'/api/tasks/{task_id}/comments')
    assert len(get_response.get_json()['comments']) == 0