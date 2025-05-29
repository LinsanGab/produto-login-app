from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from app.models import User, Product  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import bp
    app.register_blueprint(bp)

    # Cria as tabelas e o admin padrão no primeiro deploy
    with app.app_context():
        db.create_all()
        # Cria admin padrão se não existir
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')  # senha padrão
            admin.is_admin = True
            db.session.add(admin)
            db.session.commit()

    return app

