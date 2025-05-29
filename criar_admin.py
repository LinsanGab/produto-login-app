# criar_admin.py

from app.models import db, User
from werkzeug.security import generate_password_hash
from run import app  

with app.app_context():
    # Cria um usuário admin
    admin = User(
        username='admin',
        password=generate_password_hash('admin123'),
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print('✅ Usuário admin criado com sucesso!')

admin_existente = User.query.filter_by(username='admin').first()
if not admin_existente:
    db.session.add(admin)
    db.session.commit()
    print("✅ Usuário admin criado com sucesso!")
else:
    print("⚠️  Usuário admin já existe.")

