from flask import Flask, render_template, request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy


# create an app that gets named after the name of our file
app = Flask(__name__)

#for establish a connection with the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# to create the model(table )in the  databse
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    # for debuging
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

#to sync with the database to ensure all the models are created 
db.create_all()

#route todos/create listen to request that comes with method post
@app.route('/todos/create', methods =['POST'])
def create_todo():
    #to get what is written from the form in the desc square
    description = request.get_json()['description']
    #to make an new todo object
    todo = Todo (description=description)
    #establish a session to add todo
    db.session.add(todo)
    #add to database by commit
    db.session.commit()
    # redirect to the index to show the changes
    return jsonify({
        'description': todo.description
    })


# a route to listen to our home page
@app.route('/')

# the route handler
def index():
    return render_template('index.html', data=Todo.query.all())
