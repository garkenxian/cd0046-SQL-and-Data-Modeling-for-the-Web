from dal import db
from flask_migrate import Migrate

class CommonService():
    @staticmethod
    def init_db(app):
        db.init_app(app)

    def migrate_db(app):
        return Migrate(app, db)
