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
    # Use variável de ambiente para SECRET_KEY
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    # Banco de dados em /tmp para Render.com
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

    # Cria as tabelas no primeiro deploy (apenas para testes, remova em produção)
    with app.app_context():
        db.create_all()

    return app

