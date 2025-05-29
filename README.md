# 🧪 Flask Admin Dashboard

Este é um projeto em Flask com sistema de autenticação de usuários, cadastro de produtos e painel administrativo.

## 🔧 Funcionalidades

- Registro e login de usuários
- Cadastro de produtos por usuários autenticados
- Painel de administrador com:
  - Visualização de todos os usuários
  - Visualização e exclusão de produtos
  - Exclusão de usuários
- Proteção com `Flask-Login`

## 🚀 Tecnologias utilizadas

- Python 3
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite (banco local)
- Jinja2

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Rode o projeto
flask run
