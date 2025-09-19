from flask import Flask

from vetplus.extensions import db, bcrypt, login_manager, mail
from vetplus.models import User
from vetplus.routes.auth import auth_bp
from vetplus.routes.main import main_bp
from vetplus.routes.admin import admin_bp
from vetplus.routes.pets import pets_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "this-is-a-secret-key"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'contactovetplus@gmail.com'
    app.config['MAIL_PASSWORD'] = 'htfh tdyf mtex qyfw'
    app.config['MAIL_DEFAULT_SENDER'] = ('VetPlus Contacto', 'contactovetplus@gmail.com')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(pets_bp)

    with app.app_context():
        db.create_all()

        # acordarme de borrar despuess
        if not User.query.filter_by(role = "admin").first():
            hashed_pw = bcrypt.generate_password_hash("admin123").decode("utf-8")
            admin = User("admin", hashed_pw, "Administrador", "admin", "admin@gmail.com", "1111111111", "Carrera 1 # 1 - 1")
            db.session.add(admin)
            db.session.commit()
            print("Cuenta administrador creada: usuario=admin, contraseña=admin123")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug = True)