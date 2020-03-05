from settings import create_app, db
import dotenv
import os
import pytest
dotenv.load_dotenv()

os.environ['FLASK_ENV'] =  'testing'
@pytest.yield_fixture(scope='session')
def app():
    flask_app = create_app('testing')
    ctx = flask_app.app_context()
    ctx.push()
    yield flask_app
    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    yield app.test_client()



@pytest.fixture(scope='function')
def init_db(app):
    """Fixture to initialize the database"""
    with app.app_context():
        db.create_all()
        yield db
        db.session.close()
        db.drop_all()