from flask import Flask
from flask_restplus import Api
import os
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from marshmallow.exceptions import ValidationError
from api.utils.exceptions import ResponseException
import dotenv
import inspect
from config import ENV_MAPPER
import logging

db = SQLAlchemy()
dotenv.load_dotenv()

api_blueprint = Blueprint('api_bp', __name__, url_prefix='/api')
endpoint = Api(api_blueprint).route


def create_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_errors(error):
        if '_schema' in error.messages:
            error.messages = error.messages['_schema']
        return {
            'errors': error.messages,
            'message': 'Some fields are invalid'
        }, 400

    @app.errorhandler(ResponseException)
    def handle_errors(error):
        response_dict = {
            'message': error.message,
        }
        if error.errors:

            response_dict['errors'] = error.errors
        return response_dict, error.status_code

    @app.errorhandler(Exception)
    def handle_any_other_errors(error):
        logging.exception(error)
        return {'message': 'Unknown Error'}, 500


def create_app(current_env=os.getenv('FLASK_ENV', 'development')):
    app = Flask(__name__)
    origins = ['*']

    if current_env == 'development':
        import logging
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    CORS(app, origins=origins, supports_credentials=True)
    app.config.from_object(ENV_MAPPER[current_env])
    api = Api(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(api_blueprint)
    # app.register_blueprint(bp)
    import api.views
    import api.models as models

    create_error_handlers(app)

    return app
