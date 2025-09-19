from vetplus.extensions import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

vet_pet = db.Table(
    "vet_pet",
    db.Column("vet_id", db.Integer, db.ForeignKey("user.id"), primary_key = True),
    db.Column("pet_id", db.Integer, db.ForeignKey("pet.id"), primary_key = True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(20), nullable = False, default = "owner") # owner, vet, admin
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    phone = db.Column(db.String(20), nullable = False)
    address = db.Column(db.String(200), nullable = False)

    pets = db.relationship("Pet", backref = "owner", lazy = True)

    patients = db.relationship(
        "Pet",
        secondary = vet_pet,
        back_populates = "veterinarians"
    )

    def __init__(self, username, password, name, role, email, phone, address):
        self.username = username
        self.password = password
        self.name = name
        self.role = role
        self.email = email
        self.phone = phone
        self.address = address

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    species = db.Column(db.String(50), nullable = False)
    breed = db.Column(db.String(50), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    weight = db.Column(db.Float, nullable = False)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    veterinarians = db.relationship(
        "User",
        secondary = vet_pet,
        back_populates = "patients"
    )

    def __init__(self, name, species, breed, age, owner_id, weight):
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.owner_id = owner_id
        self.weight = weight

class ResetToken(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    token = db.Column(db.String(200), unique = True, nullable = False)
    expires_at = db.Column(db.DateTime, nullable = False)

    user = db.relationship("User", backref = db.backref("reset_tokens", lazy = True))