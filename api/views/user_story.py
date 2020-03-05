from settings import endpoint
from flask import request
from api.models import UserStory, User
from api.schemas import UserStorySchema, AssignUserStorySchema, StatusSchema
from .base import BaseView


@endpoint('/userstory/<string:story_id>/assign')
class UserStoryView(BaseView):
    PROTECTED_METHODS = ['POST']

    @staticmethod
    def post(story_id, user_data):
        validated_data = AssignUserStorySchema().load(request.get_json())
        user_story = UserStory.query.filter_by(
            id=story_id, created_by_id=user_data['id']).first()
        if not user_story:
            return {'message': "User story was not found"}, 404

        admin = User.query.filter_by(id=validated_data['admin_id'],
                                     is_admin=True).first()
        if not admin:
            return {'message': "The admin was not found"}, 404

        if admin.id == user_data['id']:
            return {'message': "You can't assign story to yourself"}, 400

        user_story.assignee_id = admin.id
        user_story.save()
        schema = UserStorySchema(exclude=['created_by'])
        return {
            'message': 'Assigned to admin',
            'data': schema.dump(user_story)
        }


@endpoint('/userstory/<string:story_id>/status')
class ModifyUserStoryView(BaseView):
    PROTECTED_METHODS = ['PUT']
    ADMIN_METHODS = ['PUT']

    def put(self, story_id, user_data):
        story = UserStory.query.filter_by(
            assignee_id=user_data['id'],
            id=story_id,
        ).first()
        if not story:
            return {'message': "Story not found"}, 404

        validated_data = StatusSchema().load(request.get_json())
        story.status = validated_data['status']
        story.update()
        return {
            'message': 'Successfully updated user story',
            'data': UserStorySchema().dump(story)
        }


@endpoint('/userstory')
class UserStoryView(BaseView):
    PROTECTED_METHODS = ['POST', 'GET']
    ADMIN_METHODS = ['GET']

    def get(self, user_data):
        stories = UserStory.query.filter_by(assignee_id=user.id)
        schema = UserStorySchema(many=True, exclude=['assignee'])
        return {
            'message': 'Retrieved stories successfully',
            'data': schema.dump(stories)
        }

    @staticmethod
    def post(user_data):
        schema = UserStorySchema(exclude=['created_by'])
        validated_data = schema.load(request.get_json())
        user_story = UserStory(**validated_data, created_by_id=user_data['id'])
        user_story.save()
        return {
            'message': 'Successfully created user story',
            'data': schema.dump(user_story)
        }
