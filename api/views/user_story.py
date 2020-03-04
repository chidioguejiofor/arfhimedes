from settings import endpoint
from flask import request
from flask_restplus import Resource
from api.models import UserStory, User, StatusEnum
from api.schemas import UserStorySchema, AssignUserStorySchema, StatusSchema
from api.utils.token_manager import TokenManager
import jwt


@endpoint('/userstory/<string:story_id>/assign')
class UserStoryView(Resource):
    @staticmethod
    def post(story_id):
        auth = request.headers.get('Authorization')
        if not auth:
            return {
                       'message': 'Please provided a valid token'
                   }, 401
        auth = auth.split(' ')
        if len(auth) != 2 or auth[0] != 'Bearer':
            return {
                       'message': 'Please provided a valid token'
                   }, 401
        try:
            user_data = TokenManager.decode_token_data(auth[1])
        except jwt.exceptions.PyJWTError as e:
            print(e)
            return {
                       'mesage': "Token is very invalid"
                   }, 401

        validated_data = AssignUserStorySchema().load(request.get_json())
        user_story = UserStory.query.filter_by(
            id=story_id, created_by_id=user_data['id']
        ).first()
        if not user_story:
            return {
                'message': "User story was not found"
            }, 404

        admin = User.query.filter_by(id=validated_data['admin_id'], is_admin=True).first()
        if not admin:
            return {
                'message': "The admin was not found"
            }, 404

        user_story.assignee_id = admin.id
        user_story.save()
        schema = UserStorySchema(exclude=['created_by'])
        return {
            'message': 'Assigned to admin',
            'data': schema.dump(user_story)
        }


@endpoint('/userstory/<string:story_id>/status')
class ModifyUserStoryView(Resource):
    def put(self, story_id):
        auth = request.headers.get('Authorization')
        if not auth:
            return {
                       'message': 'Please provided a valid token'
                   }, 401
        auth = auth.split(' ')
        if len(auth) != 2 or auth[0] != 'Bearer':
            return {
                       'message': 'Please provided a valid token'
                   }, 401
        try:
            user_data = TokenManager.decode_token_data(auth[1])
        except jwt.exceptions.PyJWTError as e:
            return {
                       'message': "Token is very invalid"
                   }, 401
        user = User.query.filter_by(id=user_data['id']).first()
        if not user or not user.is_admin:
            return {
                'message': 'You dont have permission to perform this action'
            }
        story = UserStory.query.filter_by(
            assignee_id=user.id,
            id=story_id,
        ).first()
        if not story:
            return {
                'message':"Story not found"
            }, 404

        validated_data = StatusSchema().load(request.get_json())
        story.status = validated_data['status']
        story.update()
        return {
            'message': 'Successfully updated user story',
            'data': UserStorySchema().dump(story)
        }




@endpoint('/userstory')
class UserStoryView(Resource):

    def get(self):
        auth = request.headers.get('Authorization')
        if not auth:
            return {
                       'message': 'Please provided a valid token'
                   }, 401
        auth = auth.split(' ')
        if len(auth) != 2 or auth[0] != 'Bearer':
            return {
                       'message': 'Please provided a valid token'
                   }, 401
        try:
            user_data = TokenManager.decode_token_data(auth[1])
        except jwt.exceptions.PyJWTError as e:
            return {
                       'mesage': "Token is very invalid"
                   }, 401

        user = User.query.filter_by(id=user_data['id']).first()
        if not user.is_admin:
            return {
                'message': 'You dont have permission to access this',
            }, 403

        stories = UserStory.query.filter_by(assignee_id=user.id)
        schema = UserStorySchema(many=True, exclude=['assignee'])
        return {
            'message': 'Retrieved stories successfully',
            'data': schema.dump(stories)
        }

    @staticmethod
    def post():
        auth = request.headers.get('Authorization')
        if not auth:
            return {
                'message': 'Please provided a valid token'
            }, 401
        auth = auth.split(' ')
        if len(auth) != 2 or auth[0] != 'Bearer' :
            return {
                'message': 'Please provided a valid token'
            }, 401
        try:
            user_data = TokenManager.decode_token_data(auth[1])
        except jwt.exceptions.PyJWTError as e:
            print(e)
            return {
                'mesage': "Token is very invalid"
            }, 401
        schema = UserStorySchema(exclude=['created_by'])
        validated_data = schema.load(request.get_json())
        user_story = UserStory(
            **validated_data,
            created_by_id=user_data['id']
        )

        user_story.save()
        return {
            'message': 'Successfully created user story',
            'data': schema.dump(user_story)
        }
