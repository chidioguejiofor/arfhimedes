import json
from api.models import User, UserStory
from api.utils.messages import (
    CREATED_USER, TIME_IN_PAST_ERROR, ASSIGNED_TO_ADMIN_SUCCESS,
    MISSING_DATA, INVALID_TOKEN, TOKEN_EXPIRED, NOT_FOUND,
    CANNOT_ASSIGN_YOURSELF, UPDATED_STORY, FORBIDDEN
)
from api.utils.token_manager import TokenManager
from faker import Faker
from datetime import datetime, timezone, timedelta

fake = Faker()
USER_STORY_URL = '/api/userstory'
ASSIGN_ADMIN_URL = '/api/userstory/{}/assign'
UPDATE_STATUS_URL = '/api/userstory/{}/status'

def add_token_to_client( expire_user_token=False, is_admin=False):
    user_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": fake.password(),
        "username": fake.simple_profile()['username'][:20],
        "email": fake.email(),
        'is_admin': is_admin
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

def create_user_story( user, assignee_id=None):
    user_story_data = {
        "complexity": 3,
        "cost": 4,
        "summary": "As a user I should be able to create a user story",
        "description": "When a user makes a call to /api/user_story, a new user story should be saved in the database",
        "type": "feature",
        "estimated_complete_time": str(datetime.now(tz=timezone.utc) + timedelta(minutes=1)),
        'assignee_id': assignee_id,
    }
    user_story = UserStory(**user_story_data, created_by_id=user.id)
    user_story.save()
    return user_story, user_story_data


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


class TestUserAssignAdminStatus:
   
    def test_create_user_story(self, init_db, client):
        user, headers = add_token_to_client()
        user_story, user_story_data = create_user_story(user)
        admin_user = User(
            username='admin101',
            email='emai@admin.com',
            first_name='Admin',
            last_name='Dogh',
            is_admin=True,
        )
        admin_user.save()
        json_data = {
            'admin_id': admin_user.id,
        }
        print(json_data)
        print(UserStory.query.first())
        response = client.post(ASSIGN_ADMIN_URL.format(user_story.id),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 200

        assert response_body['data']['complexity'] == user_story_data['complexity']
        assert response_body['data']['cost'] == user_story_data['cost']
        assert response_body['data']['summary'] == user_story_data['summary']
        assert response_body['data']['type'] == user_story_data['type']
        # assert response_body['data']['estimated_complete_time'] == json_data['estimated_complete_time']
        assert response_body['data']['assignee']['id'] == admin_user.id
        assert response_body['data']['assignee']['first_name'] == admin_user.first_name
        assert response_body['data']['assignee']['last_name'] == admin_user.last_name
        assert response_body['data']['assignee']['username'] == admin_user.username

        assert response_body['data']['status'] is None
        assert response_body['message'] == ASSIGNED_TO_ADMIN_SUCCESS

    def test_create_user_story(self, init_db, client):
        user, headers = add_token_to_client()
        user_story_data = {
            "complexity": 3,
            "cost": 4,
            "summary": "As a user I should be able to create a user story",
            "description": "When a user makes a call to /api/user_story, a new user story should be saved in the database",
            "type": "feature",
            "estimated_complete_time": str(datetime.now(tz=timezone.utc) + timedelta(minutes=1))
        }
        user_story = UserStory(**user_story_data, created_by_id=user.id)
        user_story.save()
        admin_user = User(
            username='admin101',
            email='emai@admin.com',
            first_name='Admin',
            last_name='Dogh',
            is_admin=True,
        )
        admin_user.save()
        json_data = {
            'admin_id': admin_user.id,
        }
        print(json_data)
        print(UserStory.query.first())
        response = client.post(ASSIGN_ADMIN_URL.format(user_story.id),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 200

        assert response_body['data']['complexity'] == user_story_data['complexity']
        assert response_body['data']['cost'] == user_story_data['cost']
        assert response_body['data']['summary'] == user_story_data['summary']
        assert response_body['data']['type'] == user_story_data['type']
        # assert response_body['data']['estimated_complete_time'] == json_data['estimated_complete_time']
        assert response_body['data']['assignee']['id'] == admin_user.id
        assert response_body['data']['assignee']['first_name'] == admin_user.first_name
        assert response_body['data']['assignee']['last_name'] == admin_user.last_name
        assert response_body['data']['assignee']['username'] == admin_user.username

        assert response_body['data']['status'] is None
        assert response_body['message'] == ASSIGNED_TO_ADMIN_SUCCESS
        
    def test_should_fail_when_the_required_fields_are_missing(self, init_db, client):
        user, headers = add_token_to_client()
        user_story, _ = create_user_story(user)
        admin_user = User(
            username='admin101',
            email='emai@admin.com',
            first_name='Admin',
            last_name='Dogh',
            is_admin=True,
        )
        admin_user.save()
        json_data = {}

        response = client.post(ASSIGN_ADMIN_URL.format(user_story.id),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 400

        assert response_body['errors']['admin_id'][0] == MISSING_DATA
        assert response_body['message'] == 'Some fields are invalid'

    def test_should_fail_when_the_admin_id_is_not_found(self, init_db, client):
        user, headers = add_token_to_client()
        user_story, _ = create_user_story(user)
        json_data = {
            'admin_id': 3028
        }

        response = client.post(ASSIGN_ADMIN_URL.format(user_story.id),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 404

        assert response_body['message'] == NOT_FOUND.format('Admin')

    def test_admin_user_should_not_be_able_assign_himself_a_ticket(self, init_db, client):
        user, headers = add_token_to_client()
        user_story, _ = create_user_story(user)
        user.is_admin = True
        user.update()
        json_data = {
            'admin_id': user.id
        }

        response = client.post(ASSIGN_ADMIN_URL.format(user_story.id),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 403

        assert response_body['message'] == CANNOT_ASSIGN_YOURSELF

    def test_should_fail_when_the_user_story_id_is_not_found(self, init_db, client):
        user, headers = add_token_to_client()

        admin_user = User(
            username='admin101',
            email='emai@admin.com',
            first_name='Admin',
            last_name='Dogh',
            is_admin=True,
        )
        admin_user.save()
        json_data = {
            'admin_id': admin_user.id
        }

        response = client.post(ASSIGN_ADMIN_URL.format(8293),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 404

        assert response_body['message'] == NOT_FOUND.format('User story')

    # token checks
    def test_should_fail_when_token_is_not_provided(self, init_db, client):
        user, _ = add_token_to_client(expire_user_token=True)
        user_story, _ = create_user_story(user)
        admin_user = User(
            username='admin101',
            email='emai@admin.com',
            first_name='Admin',
            last_name='Dogh',
            is_admin=True,
        )
        admin_user.save()
        headers = {
        }
        json_data = {
           'admin_id': admin_user.id
        }
        response = client.post(ASSIGN_ADMIN_URL.format(user_story.id),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 401

        assert response_body['message'] == INVALID_TOKEN

    def test_should_fail_when_token_is_expired(self, init_db, client):
        user, headers = add_token_to_client( expire_user_token=True)

        user_story, _ = create_user_story(user)
        admin_user = User(
            username='admin101',
            email='emai@admin.com',
            first_name='Admin',
            last_name='Dogh',
            is_admin=True,
        )
        admin_user.save()
        json_data = {
            'admin_id': admin_user.id
        }
        response = client.post(ASSIGN_ADMIN_URL.format(user_story.id),
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
        user, _ = add_token_to_client(expire_user_token=True)
        user_story, _ = create_user_story(user)
        admin_user = User(
            username='admin101',
            email='emai@admin.com',
            first_name='Admin',
            last_name='Dogh',
            is_admin=True,
        )
        admin_user.save()
        json_data = {
            'admin_id': admin_user.id
        }
        response = client.post(ASSIGN_ADMIN_URL.format(user_story.id),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        print(response_body)
        assert response.status_code == 401

        assert response_body['message'] == INVALID_TOKEN


class TestAdminModifiesStory:

    def test_admin_should_be_able_to_reject_user_story_status(self, init_db, client):
        admin_user, headers = add_token_to_client(is_admin=True)
        user, _ = add_token_to_client()
        user_story, user_story_data = create_user_story(user)
        json_data = {
            'status': 'REJECTED',
        }
        user_story.assignee_id = admin_user.id
        user_story.update()
        response = client.put(UPDATE_STATUS_URL.format(user_story.id),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        assert response.status_code == 200

        assert response_body['data']['complexity'] == user_story_data['complexity']
        assert response_body['data']['cost'] == user_story_data['cost']
        assert response_body['data']['summary'] == user_story_data['summary']
        assert response_body['data']['type'] == user_story_data['type']
        # assert response_body['data']['estimated_complete_time'] == json_data['estimated_complete_time']
        assert response_body['data']['assignee']['id'] == admin_user.id
        assert response_body['data']['assignee']['first_name'] == admin_user.first_name
        assert response_body['data']['assignee']['last_name'] == admin_user.last_name
        assert response_body['data']['assignee']['username'] == admin_user.username

        assert response_body['data']['status'] =='REJECTED'
        assert response_body['message'] == UPDATED_STORY


    def test_admin_should_be_able_to_approve_user_story_status(self, init_db, client):
        admin_user, headers = add_token_to_client(is_admin=True)
        user, _ = add_token_to_client()
        user_story, user_story_data = create_user_story(user)
        json_data = {
            'status': 'APPROVED',
        }
        user_story.assignee_id = admin_user.id
        user_story.update()
        response = client.put(UPDATE_STATUS_URL.format(user_story.id),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        assert response.status_code == 200

        assert response_body['data']['complexity'] == user_story_data['complexity']
        assert response_body['data']['cost'] == user_story_data['cost']
        assert response_body['data']['summary'] == user_story_data['summary']
        assert response_body['data']['type'] == user_story_data['type']
        # assert response_body['data']['estimated_complete_time'] == json_data['estimated_complete_time']
        assert response_body['data']['assignee']['id'] == admin_user.id
        assert response_body['data']['assignee']['first_name'] == admin_user.first_name
        assert response_body['data']['assignee']['last_name'] == admin_user.last_name
        assert response_body['data']['assignee']['username'] == admin_user.username

        assert response_body['data']['status'] =='APPROVED'
        assert response_body['message'] == UPDATED_STORY


    def test_should_return_not_found_when_the_admin_is_not_assigned_to_the_story(self, init_db, client):
        admin_user, headers = add_token_to_client(is_admin=True)
        user, _ = add_token_to_client()
        user_story, user_story_data = create_user_story(user)
        json_data = {
            'status': 'APPROVED',
        }
        response = client.put(UPDATE_STATUS_URL.format(user_story.id),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        assert response.status_code == 404
        response_body['message'] = NOT_FOUND.format('Story')


    def test_should_give_a_403_when_user_is_not_an_admin(self, init_db, client):
        non_admin, headers = add_token_to_client(is_admin=False)
        user, _ = add_token_to_client()
        user_story, user_story_data = create_user_story(user)
        json_data = {
            'status': 'APPROVED',
        }
        response = client.put(UPDATE_STATUS_URL.format(user_story.id),
                               data=json.dumps(json_data),
                               headers=headers,
                               content_type="application/json")
        response_body = json.loads(response.data)
        assert response.status_code == 403
        assert response_body['message'] == FORBIDDEN

