from flask_restful import Resource
from config import app,api,bcrypt,db
from flask import make_response,jsonify,request
from models import Asset, User, Assignment, Maintenance, Transaction, Requests
class Home(Resource):
    def get(self):
        response =make_response(jsonify({"message":"Welcome to Asset-Sync-Manager-Backend"}))
        return response
    
api.add_resource(Home,"/")



if __name__ == "__main__":
    app.run(debug=True,port=5555)