#Importación de atributos de la aplicación:
from app import app, db
from config import config

#Ejecución de la aplicación:
if __name__ == '__main__':
    app.config.from_object(config['development'])
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')