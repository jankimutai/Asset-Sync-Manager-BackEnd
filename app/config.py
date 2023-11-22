from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///asset.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.json.compact=False

db=SQLAlchemy()
migrate = Migrate(app,db)
db.init_app(app)

CORS(app)

bcrypt = Bcrypt(app)

api=Api(app)