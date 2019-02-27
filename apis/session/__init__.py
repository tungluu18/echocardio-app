from flask_restplus import  Resource, Namespace

api = Namespace('session')

@api.route('/')
class Session(Resource):
    @api.doc('list session')
    def get(self):
        return "Day la mot session"
