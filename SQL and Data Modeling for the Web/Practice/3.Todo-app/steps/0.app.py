from flask import Flask, render_template

# create an app that gets named after the name of our file
app = Flask(__name__)

# a route to listen to our home page


@app.route('/')
# tehh route handler
def index():
    return render_template('index.html', data=[{
        'description': 'Todo 1'
    }, {
        'description': 'Todo 2'
    }, {
        'description': 'Todo 3'
    }])
