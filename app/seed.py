from config import app,db, bcrypt
from models import Asset, User, Assignment, Maintenance, Transaction, Requests
from faker import Faker
from random import choice as rc
from datetime import datetime
fake = Faker()

with app.app_context():
    Asset.query.delete()
    User.query.delete()
    Assignment.query.delete()
    Maintenance.query.delete()
    Transaction.query.delete()
    Requests.query.delete()

    print('Deleting existing data from databases')

    
    laptop_models = ["Latitude 1", "ThinkPad 1", "XPS 1", "MacBook 1", "Surface 1", "Latitude 2", "ThinkPad 2", "XPS 2", "MacBook 2", "Surface 2", "Latitude 3", "ThinkPad 3", "XPS 3", "MacBook 3", "Surface 3", "Latitude 4", "ThinkPad 4", "XPS 4", "MacBook 4", "Surface 4"]
    desktop_models = ["OptiPlex 1", "OptiPlex 2", "OptiPlex 3", "OptiPlex 4", "Inspiron 1", "Inspiron 2", "Inspiron 3", "Inspiron 4", "iMac 1", "iMac 2", "iMac 3", "iMac 4", "Precision 1", "Precision 2", "Precision 3", "Precision 4"]
    server_models = ["Dell PowerEdge R640", "Dell PowerEdge R740", "Dell PowerEdge R740xd", "Dell PowerEdge T640","Dell PowerEdge R650","Dell PowerEdge R750","Dell PowerEdge R850","Dell PowerEdge T440","Dell PowerEdge R760xa","Dell PowerEdge R760xa","Dell PowerEdge R760xd2","Dell PowerEdge R860"]
    router_models = ["Linksys Hydra Pro 6", "Linksys RV320", "Linksys RV325", "Linksys RV325","Cisco Catalyst IR1100 Rugged Series","Cisco Catalyst IR8100 Heavy Duty Series","Cisco 500 Series WPAN Industrial Routers","Netgear Orbi Mesh WiFi System (AC1200)","TP-Link Archer AX21","TP-Link Archer AX55","TP-Link Archer AXE75"]

    it_equipments = []

    for i in range(30):
        category = rc(['Laptop', 'Desktop', 'Server', 'Router'])

        if category == 'Laptop':
            model_name = rc(laptop_models)
        elif category == 'Desktop':
            model_name = rc(desktop_models)
        elif category == 'Server':
            model_name = rc(server_models)
        elif category == 'Router':
            model_name = rc(router_models)
     

        manufacturer = fake.company()
        image_url = fake.image_url()

        equipment_instance = Asset(
            model=model_name.split()[0],
            asset_name=model_name,
            date_purchased=datetime.utcnow(),
            image_url=image_url,
            manufacturer=manufacturer,
            created_at=fake.date_time(),
            status=rc(['Active', 'Pending', 'Under Maintenance']),
            category=category,
            quantity=fake.random_int(min=1, max=30)
        )

        it_equipments.append(equipment_instance)

        db.session.add_all(it_equipments)
        db.session.commit()

    print('Generating assets')

    users = []

    for i in range(4):
        fake_password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        hashed_password = bcrypt.generate_password_hash(fake_password).decode('utf-8')

        user = User(
            full_name=fake.name(),
            username=fake.user_name(),
            email=fake.email(),
            _password_hash=hashed_password,
            employed_on=fake.date_between(start_date="-2y", end_date="today"),
            role=rc(['Normal Employee', 'Admin', 'Procurement Manager']),
            department=rc(["Marketing","Finance","Human Resource","Management","Operations","Audit","IT"])
        )

        users.append(user)
        db.session.add_all(users)
    db.session.commit()

    print('Generating users')

    assigned_assets = set()
    for _ in range(12):
        available_assets = Asset.query.filter(Asset.id.notin_(assigned_assets)).all()
        if not available_assets:
            break  # No more available assets to assign
        assignment_asset = rc(available_assets)
        assigned_assets.add(assignment_asset.id)
        assignment = Assignment(
            asset=assignment_asset,
            user=User.query.order_by(db.func.random()).first(),
            assignment_date=fake.date_between(start_date="-1y", end_date="today"),
            return_date=fake.date_between(start_date="today", end_date="+1y"),
    )
        db.session.add(assignment)
    db.session.commit()

    print('Generating assignments')
    
    assets_under_maintenance = set()
    for _ in range(21):
        available_assets = Asset.query.filter(Asset.id.notin_(assets_under_maintenance)).all()

        if not available_assets:
            break  # No more available assets for maintenance

        maintenance_asset = rc(available_assets)
        assets_under_maintenance.add(maintenance_asset.id)

        maintenance = Maintenance(
            asset_id=maintenance_asset.id,
            date_of_maintenance=fake.date_between(start_date="-2y", end_date="today"),
            type=rc(['Scheduled', 'Unscheduled']),
            description=fake.text(),
        )
        db.session.add(maintenance)

        # Update the asset status to 'Under Maintenance'
        maintenance_asset.status = 'Under Maintenance'

    db.session.commit()
    print('Generating maintenance records')

    transaction_types = ['Purchase', 'Transfer', 'Maintenance', 'Sale']
    sold_assets = set()  # Keep track of assets that have been sold

    for _ in range(21):
        transaction_type = rc(transaction_types)
        available_assets = Asset.query.filter(Asset.id.notin_(sold_assets)).all()

        asset = rc(available_assets) if available_assets else None

        if transaction_type == 'Purchase':
            if asset:
                asset.quantity += fake.random_int(min=1, max=10)
            else:
                asset = Asset(
                    model=model_name.split()[0],
                    asset_name=model_name,
                    date_purchased=datetime.utcnow(),
                    image_url=fake.image_url(),
                    manufacturer=fake.company(),
                    created_at=fake.date_time(),
                    status=rc(['Active', 'Pending', 'Under Maintenance']),
                    category=category,
                    quantity=fake.random_int(min=1, max=30)
                )
                db.session.add(asset)

        elif transaction_type == 'Sale':
            if asset and asset.quantity > 0:
                asset.quantity -= fake.random_int(min=1, max=asset.quantity)
                sold_assets.add(asset.id)

        elif transaction_type == 'Maintenance':
            if asset:
                existing_maintenance = Maintenance.query.filter_by(asset_id=asset.id).first()

                if not existing_maintenance:
                    maintenance = Maintenance(
                        asset_id=asset.id,
                        date_of_maintenance=fake.date_between(start_date="-2y", end_date="today"),
                        type=rc(['Scheduled', 'Unscheduled']),
                        description=fake.text(),
                    )
                    db.session.add(maintenance)

                    # Update the asset status to 'Under Maintenance'
                    asset.status = 'Under Maintenance'

        elif transaction_type == 'Transfer':
            if asset:
                existing_transaction = Transaction.query.filter_by(asset_id=asset.id).first()

                if not existing_transaction:
                    new_user = User.query.order_by(db.func.random()).first()

                    existing_assignment = Assignment.query.filter_by(asset_id=asset.id).first()

                    if existing_assignment:
                        existing_assignment.user_id = new_user.id
                        existing_assignment.assignment_date = fake.date_between(start_date="-1y", end_date="today")
                        existing_assignment.return_date = fake.date_between(start_date="today", end_date="+1y")
                    else:
                        new_assignment = Assignment(
                            asset=asset,
                            user=new_user,
                            assignment_date=fake.date_between(start_date="-1y", end_date="today"),
                            return_date=fake.date_between(start_date="today", end_date="+1y"),
                        )
                        db.session.add(new_assignment)

            
        if asset:
            transaction = Transaction(
                asset=asset,
                transaction_type=transaction_type,
                transaction_date=fake.date_between(start_date="-1y", end_date="today"),
                )
            db.session.add(transaction)
        db.session.commit()

    # Common block for all transaction types
    if asset:
        transaction = Transaction(
            asset=asset,
            transaction_type=transaction_type,
            transaction_date=fake.date_between(start_date="-1y", end_date="today"),
        )
        db.session.add(transaction)

    db.session.commit()
 



    print('Generating transactions')

    asset_names = ['Laptop', 'Desktop', 'Printer', 'Scanner', 'Projector', 'Phone', 'Tablet']
    for _ in range(20):
        request = Requests(
            user=User.query.order_by(db.func.random()).first(),
            asset_name=rc(asset_names),
            description=fake.text(),
            quantity=fake.random_int(min=1, max=13),
            urgency=rc(['High', 'Medium', 'Low']),
            status="Pending"
        )
        db.session.add(request)
    db.session.commit()


    print('Generating requests')

    print('Done seeding...')
