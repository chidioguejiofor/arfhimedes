from settings import endpoint
from flask_restplus import Resource

@endpoint('/sample')
class Sample(Resource):
    @staticmethod
    def get():
        return {
            'here':"here we go213!"
        }
