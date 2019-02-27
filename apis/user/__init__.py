from flask_restplus import  Resource, Namespace

api = Namespace('user')

@api.route('/')
class User(Resource):
    @api.doc('list user')
    def get(self):
        return "Ahihi"
