import json
from api.models import User, UserStory
from api.utils.messages import CREATED_USER, TIME_IN_PAST_ERROR,MISSING_DATA, INVALID_TOKEN, TOKEN_EXPIRED
from api.utils.token_manager import TokenManager
from faker import Faker
from datetime import datetime, timezone, timedelta
fake = Faker()
USER_STORY_URL = '/api/userstory'
ASSIGN_ADMIN_URL = '/api/userstory/{}/assign'

def add_token_to_client( expire_user_token=False):
    user_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": fake.password(),
        "username": "user311",
        "email": "email111@email.com"
    }
    seconds = 50
    if expire_user_token:
        seconds =-1
    user = User(**user_data)
    user.save()
    token = TokenManager.create_token({
        'id': user.id,
        'email': user.email,
    }, seconds=seconds)
    return user, {
        'Authorization': f'Bearer {token}'
    }

class TestCreateUserStory:
    def test_create_user_story(self, init_db, client):
        user, headers = add_token_to_client()
        json_data = {
            "complexity": 3,
            "cost": 4,
            "summary": "As a user I should be able to create a user story",
            "description": "When a user makes a call to /api/user_story, a new user story should be saved in the database",
            "type":"feature",
            "estimated_complete_time":str(datetime.now(tz=timezone.utc) + timedelta(minutes=1))
        }
        response = client.post(USER_STORY_URL,
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 201

        assert response_body['data']['complexity'] == json_data['complexity']
        assert response_body['data']['cost'] == json_data['cost']
        assert response_body['data']['summary'] == json_data['summary']
        assert response_body['data']['type'] == json_data['type']
        # assert response_body['data']['estimated_complete_time'] == json_data['estimated_complete_time']
        assert response_body['data']['assignee'] is None
        assert response_body['data']['status'] is None
        assert response_body['message'] == CREATED_USER

    def test_should_fail_when_estimated_time_is_in_the_past(self, init_db, client):
        user, headers = add_token_to_client()
        json_data = {
            "complexity": 3,
            "cost": 4,
            "summary": "As a user I should be able to create a user story",
            "description": "When a user makes a call to /api/user_story, a new user story should be saved in the database",
            "type":"feature",
            "estimated_complete_time": str(datetime.now(tz=timezone.utc) - timedelta(seconds=1))
        }
        response = client.post(USER_STORY_URL,
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 400

        assert response_body['errors']['estimated_complete_time'][0] ==TIME_IN_PAST_ERROR
        assert response_body['message'] == "Some fields are invalid"

    def test_should_fail_when_required_fields_are_missing(self, init_db, client):
        user, headers = add_token_to_client()
        json_data = {}
        response = client.post(USER_STORY_URL,
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        assert response.status_code == 400
        assert response_body['errors']['description'][0] == MISSING_DATA
        assert response_body['errors']['summary'][0] == MISSING_DATA
        assert response_body['errors']['type'][0] == MISSING_DATA
        assert response_body['message'] == "Some fields are invalid"

    def test_should_fail_when_token_is_not_provided(self, init_db, client):
        user, headers = add_token_to_client()
        headers = {
        }
        json_data = {
            "complexity": 3,
            "cost": 4,
            "summary": "As a user I should be able to create a user story",
            "description": "When a user makes a call to /api/user_story, a new user story should be saved in the database",
            "type": "feature",
            "estimated_complete_time": str(datetime.now(tz=timezone.utc) - timedelta(seconds=1))
        }
        response = client.post(USER_STORY_URL,
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 401

        assert response_body['message'] == INVALID_TOKEN

    def test_should_fail_when_token_is_expired(self, init_db, client):
        user, headers = add_token_to_client( expire_user_token=True)
        json_data = {
            "complexity": 3,
            "cost": 4,
            "summary": "As a user I should be able to create a user story",
            "description": "When a user makes a call to /api/user_story, a new user story should be saved in the database",
            "type": "feature",
            "estimated_complete_time": str(datetime.now(tz=timezone.utc) - timedelta(seconds=1))
        }
        response = client.post(USER_STORY_URL,
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 401

        assert response_body['message'] == TOKEN_EXPIRED


    def test_should_fail_when_token_does_not_have_the_valid_format(self, init_db, client):
        headers = {
            'Authorization': 'v'
        }
        json_data = {
            "complexity": 3,
            "cost": 4,
            "summary": "As a user I should be able to create a user story",
            "description": "When a user makes a call to /api/user_story, a new user story should be saved in the database",
            "type": "feature",
            "estimated_complete_time": str(datetime.now(tz=timezone.utc) - timedelta(seconds=1))
        }
        response = client.post(USER_STORY_URL,
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 401

        assert response_body['message'] == INVALID_TOKEN


