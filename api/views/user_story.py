from settings import endpoint
from flask import request
from flask_restplus import Resource
from api.models import UserStory, User
from api.schemas import UserStorySchema, AssignUserStorySchema
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


@endpoint('/userstory')
class UserStoryView(Resource):
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
