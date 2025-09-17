from vetplus.extensions import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(20), nullable = False, default = "owner") # owner, vet, admin
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    phone = db.Column(db.String(20), nullable = False)
    address = db.Column(db.String(200), nullable = False)

    def __init__(self, username, password, name, role, email, phone, address):
        self.username = username
        self.password = password
        self.name = name
        self.role = role
        self.email = email
        self.phone = phone
        self.address = address