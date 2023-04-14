from app import app, db
from config import config

if __name__ == '__main__':
    app.config.from_object(config['development'])
    with app.app_context():
        db.create_all()
    app.run()