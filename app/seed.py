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

    
    assets =[]

    for i in range(50):
        asset = Asset(
            assetName=fake.word(),
            model=fake.word(),
            imageUrl=fake.image_url(),  # Use Faker's image_url to generate image URLs
            manufacturer=fake.word(),
            datePurchased=fake.date_time(),
            status=rc(['Active', 'Pending', 'Under Maintenance']),
            category=fake.word()
        )

        assets.append(asset)
        db.session.add_all(assets)
        db.session.commit()

    print('Generating assets')