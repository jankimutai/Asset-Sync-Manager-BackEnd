from flask_restful import Resource,reqparse
from psycopg2 import IntegrityError
from config import app,api,bcrypt,db
from flask import make_response,jsonify,request,session
from models import Asset, User, Assignment, Maintenance, Transaction, Requests
class Home(Resource):
    def get(self):
        response =make_response(jsonify({"message":"Welcome to Asset-Sync-Manager-Backend"}))
        return response
    
api.add_resource(Home,"/")
class Login(Resource):
   def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        user = User.query.filter_by(email=args['email']).first()

        if user and user.authenticate(args['password']):
            session["user_id"]=user.id
            return make_response(jsonify({'message': 'Login successful'}, 200))
        else:
            return make_response(jsonify({'error': 'Invalid username or password'}, 401))
api.add_resource(Login,"/login")
class Registration(Resource):
   def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('full_name', type=str, required=True, help='Full name is required')
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        parser.add_argument('role', type=str, required=True, help='Role is required')
        parser.add_argument('department', type=str, required=True, help='Department is required')

        args = parser.parse_args()

        new_user = User(
            full_name=args['full_name'],
            username=args['username'],
            email=args['email'],
            role=args['role'],
            department=args['department']
        )

        new_user.password_hash = str(args.get('password'))

        try:
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({'message': 'User registered successfully'}), 201)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'error': 'Username or email already exists'}), 409)

api.add_resource(Registration,"/registration")
class Assets(Resource):
    def get(self):
        assets = [asset.to_dict() for asset in Asset.query.all()]
        response= make_response(jsonify(assets), 200)
        return response
    def post(self):
        data = request.get_json()

        new_asset = Asset(
            asset_name=data['asset_name'],
            model=data['model'],
            image_url=data.get('image_url'),
            manufacturer=data.get('manufacturer'),
            date_purchased=data.get('date_purchased'),
            status=data.get('status'),
            category=data.get('category')
        )

        try:
            db.session.add(new_asset)
            db.session.commit()
            return make_response(jsonify({'message': 'Asset created successfully'}), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 400)
api.add_resource(Assets,"/assets")
class AssetById(Resource):
    def get(self, asset_id):
        asset = Asset.query.filter_by(id=asset_id).first()

        if not asset:
            return make_response(jsonify({'error': 'Asset not found'}), 404)

        return make_response(jsonify(asset.to_dict()), 200)


    def put(self, asset_id):
        asset = Asset.query.filter_by(id=asset_id).first()
        data = request.get_json()

        asset.asset_name = data.get('asset_name', asset.asset_name)
        asset.model = data.get('model', asset.model)
        asset.image_url = data.get('image_url', asset.image_url)
        asset.manufacturer = data.get('manufacturer', asset.manufacturer)
        asset.date_purchased = data.get('date_purchased', asset.date_purchased)
        asset.status = data.get('status', asset.status)
        asset.category = data.get('category', asset.category)

        try:
            db.session.commit()
            return make_response(jsonify({'message': 'Asset updated successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 400)

    def delete(self, asset_id):
        asset = Asset.query.get_or_404(asset_id)

        try:
            db.session.delete(asset)
            db.session.commit()
            return make_response(jsonify({'message': 'Asset deleted successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 400)

api.add_resource(AssetById,'/assets/<int:asset_id>')

class admin_dashboard(Resource):
    def get(self):
        pass

api.add_resource(admin_dashboard,"/admin/dashboard")
class user_dashboard(Resource):
    def get(self):
        pass
api.add_resource(user_dashboard,"/user/dashboard")



if __name__ == "__main__":
    app.run(debug=True,port=5555)