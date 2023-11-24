from config import db, bcrypt
from models import Asset, User, Assignment, Maintenance, Transaction, Requests
from faker import Faker
from random import choice as rc

fake = Faker()

with db.app.app_context():
    Asset.query.delete()
    User.query.delete()
    Assignment.query.delete()
    Maintenance.query.delete()
    Transaction.query.delete()
    Requests.query.delete()

    print('Deleting existing data from databases')