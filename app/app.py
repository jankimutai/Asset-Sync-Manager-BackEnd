from flask_restful import Resource
from config import app,api,bcrypt
from flask import make_response,jsonify,request

class Home(Resource):
    def get(self):
        response =make_response(jsonify({"message":"Welcome to Asset-Sync-Manager-Backend"}))
        return response
    
api.add_resource(Home,"/")



if __name__ == "__main__":
    app.run(debug=True,port=5555)