from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from database.models import db
from config import Config

migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.blueprints.main.routes import main_bp
    from app.blueprints.auth.routes import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app