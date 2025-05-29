from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Product
from app import db
from flask import session



bp = Blueprint('main', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            if user.is_admin:
                return redirect(url_for('main.admin_panel'))  
            else:
                return redirect(url_for('main.dashboard'))    
        else:
            flash('Usuário ou senha inválidos.', 'danger')
            return redirect(url_for('main.login'))  

    
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Limpa toda a sessão para garantir
    flash('Você saiu com sucesso.', 'success')
    return redirect(url_for('main.login'))

# Área protegida
@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Redireciona a raiz para a página de login
@bp.route('/')
def index():
    return redirect(url_for('main.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se usuário já existe
        if User.query.filter_by(username=username).first():
            flash('Usuário já existe.', 'danger')
            return redirect(url_for('main.register'))

        # Cria o usuário com a senha criptografada
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Usuário criado com sucesso! Faça login.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        new_product = Product(name=name, description=description, owner=current_user)
        db.session.add(new_product)
        db.session.commit()

        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_product.html')
# Rota para o painel do administrador
@bp.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash("Acesso restrito ao administrador.", "danger")
        return redirect(url_for('main.dashboard'))

    users = User.query.filter(User.id != current_user.id).all()
    products = Product.query.all()
    return render_template('admin_panel.html', users=users, products=products)


@bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("Acesso negado.", "danger")
        return redirect(url_for('main.dashboard'))

    user = User.query.get_or_404(user_id)

    # Remove os produtos do usuário
    for product in user.products:
        db.session.delete(product)

    db.session.delete(user)
    db.session.commit()
    flash("Usuário e seus produtos foram removidos.", "success")
    return redirect(url_for('main.admin_panel'))


@bp.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash("Acesso negado.", "danger")
        return redirect(url_for('main.dashboard'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Produto removido com sucesso.", "success")
    return redirect(url_for('main.admin_panel'))
