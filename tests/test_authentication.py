import json
from api.models import User
from api.utils.messages import (
    SIGN_UP_SUCCESS, USER_ALREADY_EXISTS, MISSING_DATA,
    LOGIN_SUCCESS, LOGIN_FAILED
)
from faker import Faker

fake = Faker()
REGISTER_URL = '/api/register'
LOGIN_URL = '/api/login'

class TestRegister:
    def test_user_should_be_able_to_register_with_valid_data(self, init_db, client):
        json_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": fake.password(),
            "username": "user123",
            "email": "email111@email.com"
        }

        response = client.post(REGISTER_URL,
                               data=json.dumps(json_data),
                               content_type="application/json")
        assert response.status_code == 201
        response_body = json.loads(response.data)
        assert response_body['data']['username'] == json_data['username']
        assert response_body['data']['first_name'] == json_data['first_name']
        assert response_body['data']['last_name'] == json_data['last_name']
        assert response_body['data']['email'] == json_data['email']
        assert response_body['data']['is_admin'] is False
        assert response_body['message'] == SIGN_UP_SUCCESS

    def test_signup_fails_when_username_already_exists(self, init_db, client):
        json_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": fake.password(),
            "username": "user311",
            "email": "email111@email.com"
        }
        User(**json_data).save()
        response = client.post(REGISTER_URL,
                               data=json.dumps(json_data),
                               content_type="application/json")
        assert response.status_code == 409
        response_body = json.loads(response.data)
        assert 'data' not in response_body
        assert response_body['message'] == USER_ALREADY_EXISTS

    def test_returns_400_when_no_data_is_provided(self, init_db, client):
        json_data = {}
        response = client.post(REGISTER_URL,
                               data=json.dumps(json_data),
                               content_type="application/json")
        assert response.status_code == 400
        response_body = json.loads(response.data)
        assert response_body['errors']['username'][0] == MISSING_DATA
        assert response_body['errors']['first_name'][0] == MISSING_DATA
        assert response_body['errors']['last_name'][0] == MISSING_DATA
        assert response_body['errors']['email'][0] == MISSING_DATA
        assert response_body['message'] == 'Some fields are invalid'



class TestLogin:
    def test_login_should_be_able_to_login_with_username_when_user_is_found(self, init_db, client):
        user_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": fake.password(),
            "username": "user123",
            "email": "email111@email.com"
        }

        User(**user_data).save()
        json_data = {
            "username_or_email": "user123",
            "password":user_data['password'],
        }

        response = client.post(LOGIN_URL,
                               data=json.dumps(json_data),
                               content_type="application/json")
        assert response.status_code == 200
        response_body = json.loads(response.data)
        assert response_body['data']['username'] == user_data['username']
        assert response_body['data']['first_name'] == user_data['first_name']
        assert response_body['data']['last_name'] == user_data['last_name']
        assert response_body['data']['email'] == user_data['email']
        assert response_body['data']['is_admin'] is False
        assert response_body['message'] == LOGIN_SUCCESS

    def test_login_should_be_able_to_login_with_email_when_user_is_found(self, init_db, client):
        user_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": fake.password(),
            "username": "user123",
            "email": "email111@email.com"
        }

        User(**user_data).save()
        json_data = {
            "username_or_email": "email111@email.com",
            "password": user_data['password'],
        }

        response = client.post(LOGIN_URL,
                               data=json.dumps(json_data),
                               content_type="application/json")
        assert response.status_code == 200
        response_body = json.loads(response.data)
        assert response_body['data']['username'] == user_data['username']
        assert response_body['data']['first_name'] == user_data['first_name']
        assert response_body['data']['last_name'] == user_data['last_name']
        assert response_body['data']['email'] == user_data['email']
        assert response_body['data']['is_admin'] is False
        assert response_body['message'] == LOGIN_SUCCESS

    def test_login_should_fail_when_password_is_invalid(self, init_db, client):
        user_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": fake.password(),
            "username": "user123",
            "email": "email111@email.com"
        }

        User(**user_data).save()
        json_data = {
            "username_or_email": "email111@email.com",
            "password": 'invalid_password',
        }
        response = client.post(LOGIN_URL,
                               data=json.dumps(json_data),
                               content_type="application/json")
        assert response.status_code == 404
        response_body = json.loads(response.data)
        assert 'data' not in response_body
        assert response_body['message'] == LOGIN_FAILED



    def test_login_should_fail_when_username_is_invalid(self, init_db, client):
        user_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": fake.password(),
            "username": "user123",
            "email": "email111@email.com"
        }

        User(**user_data).save()
        json_data = {
            "username_or_email": "unknown_username",
            "password": user_data['password'],
        }
        response = client.post(LOGIN_URL,
                               data=json.dumps(json_data),
                               content_type="application/json")
        assert response.status_code == 404
        response_body = json.loads(response.data)
        assert 'data' not in response_body
        assert response_body['message'] == LOGIN_FAILED

    def test_login_should_fail_when_email_is_not_found(self, init_db, client):
        user_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": fake.password(),
            "username": "user123",
            "email": "email111@email.com"
        }

        User(**user_data).save()
        json_data = {
            "username_or_email": "email@mail.com",
            "password": user_data['password'],
        }
        response = client.post(LOGIN_URL,
                               data=json.dumps(json_data),
                               content_type="application/json")
        assert response.status_code == 404
        response_body = json.loads(response.data)
        assert 'data' not in response_body
        assert response_body['message'] == LOGIN_FAILED

    def test_returns_400_when_no_data_is_provided(self, init_db, client):
        json_data = {}
        response = client.post(LOGIN_URL,
                               data=json.dumps(json_data),
                               content_type="application/json")
        assert response.status_code == 400
        response_body = json.loads(response.data)
        assert response_body['errors']['username_or_email'][0] == MISSING_DATA
        assert response_body['errors']['password'][0] == MISSING_DATA

