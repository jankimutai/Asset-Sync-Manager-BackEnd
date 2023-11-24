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
            imageUrl=fake.image_url(),  
            manufacturer=fake.word(),
            datePurchased=fake.date_time(),
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
            fullName=fake.name(),
            username=fake.user_name(),
            email=fake.email(),
            password_hash=hashed_password,
            role=fake.word(),
            department=fake.word()
        )

        users.append(user)
        db.session.add_all(users)
        db.session.commit()

    print('Generating users')

    assignments = []

    for _ in range(20):
        assignment = Assignment(
            asset=rc(assets),
            user=rc(users),
            assignmentDate=fake.date_time(),
            returnDate=fake.date_time()
        )

        assignments.append(assignment)
        db.session.add_all(assignments)
        db.session.commit()

    print('Generating assignments')

    maintenances = []

    for _ in range(15):
        maintenance = Maintenance(
            asset=rc(assets),
            dateofmaintenance=fake.date_time(),
            type=fake.word(),
            description=fake.text()
        )

        maintenances.append(maintenance)
        db.session.add_all(maintenances)
        db.session.commit()

    print('Generating maintenance records')


    transactions = []

    for _ in range(30):
        transaction = Transaction(
            asset=rc(assets),
            transactionDate=fake.date_time(),
            transactiontype=fake.word()
        )

        transactions.append(transaction)
        db.session.add_all(transactions)
        db.session.commit()

    print('Generating transactions')
