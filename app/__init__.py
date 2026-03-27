from flask import Flask

def create_app():
    app = Flask(__name__)

    # 🔐 Chave secreta (em produção o ideal é usar variável de ambiente)
    app.config['SECRET_KEY'] = 'chave_secreta'

    # 📦 Registro de rotas (Blueprint)
    from .routes import main
    app.register_blueprint(main)

    return app