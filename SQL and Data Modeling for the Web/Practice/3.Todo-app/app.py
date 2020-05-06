from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
# 1. import migartion
from flask_migrate import Migrate

# create an app that gets named after the name of our file
app = Flask(__name__)

# for establish a connection with the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 2.start using flask migrate initilize down and up grade
migrate = Migrate(app, db)
# 3.intial migration flask db init
# 4.flask db migrate


# to create the model(table )in the  databse
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey(
        'todolists.id'), nullable=False)

    # for debuging
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

# creating a new model to categorize the todos object


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

# to sync with the database to ensure all the models are created
# db.create_all()

# route todos/create listen to request that comes with method post
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        # to get what is written from the form in the desc square
        description = request.get_json()['description']
        # to make an new todo object
        todo = Todo(description=description)
        # establish a session to add todo
        db.session.add(todo)
        # add to database by commit
        db.session.commit()
        # redirect to the index to show the changes
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

# route to the update events
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

# route for delete an object
@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})

# a route to listen to our home page
@app.route('/lists/<list_id>')
# the route handler
def get_list_todos(list_id):
    return render_template('index.html',
        lists=TodoList.query.all(),
        active_list = TodoList.query.get(list_id),
        todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())


@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))
