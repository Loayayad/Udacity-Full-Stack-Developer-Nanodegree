from flask import Flask, jsonify
from models import setup_db, Plant
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route("/hello")
    @cross_origin()
    def get_greeting():
        return jsonify({'message': 'Hello, World!'})

    # a simple page that says hello
    # @app.route('/')
    # def hello():
    #    return jsonify({'message': 'HELLO WORLD'})

    @app.route('/smiley')
    def smiley():
        return ':)'

    @app.route('/plants')
    def get_plants():
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        return jsonify({
            'success': True,
            'plants':formatted_plants,
        })

    @app.route('/entrees/<int:entree_id>')
    def retrieve_entree(entree_id):
        return 'Entree %d' % entree_id
