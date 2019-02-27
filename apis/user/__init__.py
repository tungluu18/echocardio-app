from flask_restplus import  Resource, Api, Namespace

api = Namespace('user')

@api.route('/')
class User(Resource):
    @api.doc('list user')
    def get(self):
        return "Ahihi"
