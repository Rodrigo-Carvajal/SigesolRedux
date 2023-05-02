#Importación de librerías utilizadas en el backend:
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from config import config
from flask_wtf.csrf import CSRFProtect

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = './sigesolV4/app/static/docs'

#Instanciación de objetos para la aplicación
app = Flask(__name__)
app.secret_key = '484267d6-5754-4b52-b66e-7da05e5ab7bd'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/sigesol2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy()
login_manager = LoginManager(app)
login_manager.init_app(app)
db.init_app(app)

#Importación de blueprint:
from app.controllers import sigesolBP
app.register_blueprint(sigesolBP)