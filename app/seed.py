from config import app,db, bcrypt
from models import Asset, User, Assignment, Maintenance, Transaction, Requests
from faker import Faker
from random import choice as rc

fake = Faker()

with app.app_context():
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
            asset_name=fake.word(),
            model=fake.word(),
            image_url=fake.image_url(),  
            manufacturer=fake.company(),
            date_purchased=fake.date_time(),
            status=rc(['Active', 'Pending', 'Under Maintenance']),
            category=fake.word()
        )

        assets.append(asset)
        db.session.add_all(assets)
        db.session.commit()

    print('Generating assets')

    users = []

    for i in range(30):
        fake_password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        hashed_password = bcrypt.generate_password_hash(fake_password).decode('utf-8')

        user = User(
            full_name=fake.name(),
            username=fake.user_name(),
            email=fake.email(),
            _password_hash=hashed_password,
            role=fake.word(),
            department=rc(["Marketing","Finance","Human Resource","Management","Operations","Audit","IT"])
        )

        users.append(user)
        db.session.add_all(users)
        db.session.commit()

    print('Generating users')


    for _ in range(30):
        assignment = Assignment(
            asset=Asset.query.order_by(db.func.random()).first(),
            user=User.query.order_by(db.func.random()).first(),
            assignment_date=fake.date_between(start_date="-30d", end_date="today"),
            return_date=fake.date_between(start_date="today", end_date="+30d"),
    )
        db.session.add(assignment)
    db.session.commit()


       

    print('Generating assignments')

    for _ in range(30):
        
        maintenance = Maintenance(
            asset=Asset.query.order_by(db.func.random()).first(),
            date_of_maintenance=fake.date_between(start_date="-30d", end_date="today"),
            type=fake.word(),
            description=fake.text(),
        )

        
        db.session.add(maintenance)
        db.session.commit()


    print('Generating maintenance records')


    for _ in range(20):
        
        transaction = Transaction(
            asset=Asset.query.order_by(db.func.random()).first(),
            transaction_date=fake.date_between(start_date="-30d", end_date="today"),
            transaction_type=fake.word(),
        )
        db.session.add(transaction)
        db.session.commit()

    print('Generating transactions')

    for _ in range(21):
        request = Requests(
            user=User.query.order_by(db.func.random()).first(),
            description=fake.text(),
            status=fake.random_element(elements=("Pending", "Approved", "Rejected")),
            asset_name=fake.word(),
        )
        db.session.add(request)
        db.session.commit()

    print('Generating requests')

    print('Done seeding...')
