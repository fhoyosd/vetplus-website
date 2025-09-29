from vetplus.extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

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

    pets = db.relationship("Pet", backref = "owner", cascade = "all, delete-orphan")

    patients = db.relationship(
        "Pet",
        secondary = vet_pet,
        back_populates = "veterinarians"
    )

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    species = db.Column(db.String(50), nullable = False)
    breed = db.Column(db.String(50), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    weight = db.Column(db.Float, nullable = False)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete = "CASCADE"), nullable = False)

    veterinarians = db.relationship(
        "User",
        secondary = vet_pet,
        back_populates = "patients"
    )

class ResetToken(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    token = db.Column(db.String(200), unique = True, nullable = False)
    expires_at = db.Column(db.DateTime, nullable = False)

    user = db.relationship("User", backref = db.backref("reset_tokens", lazy = True))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    description = db.Column(db.String(200), nullable = True)

    products = db.relationship("Product", backref = "category", lazy = True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = False)
    price = db.Column(db.Float, nullable = False)
    stock = db.Column(db.Integer, nullable = False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable = False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    full_name = db.Column(db.String(150), nullable = False)
    address = db.Column(db.String(200), nullable = False)
    phone = db.Column(db.String(20), nullable = False)

    payment_method = db.Column(db.String(50), nullable = False)

    card_number = db.Column(db.String(20), nullable = True)
    card_expiry = db.Column(db.String(7), nullable = True)

    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    total = db.Column(db.Float, nullable = False)
    status = db.Column(db.String(20), default = "pending")  # pending, paid, cancelled

    user = db.relationship("User", backref = "orders")
    details = db.relationship("OrderDetail", backref = "order", cascade = "all, delete-orphan")

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable = False)

    quantity = db.Column(db.Integer, nullable = False)
    subtotal = db.Column(db.Float, nullable = False)

    product = db.relationship("Product")

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombredemascota = db.Column(db.String(100), nullable = False)
    nombrededueno = db.Column(db.String(100), nullable = False)
    datosdeconsulta = db.Column(db.Text, nullable = False)
    hora = db.Column(db.String(20), nullable = False)
    veterinario = db.Column(db.String(100), nullable = False)
    registros = db.relationship("RegistroMedico", back_populates = "consulta", cascade = "all, delete-orphan")

class RegistroMedico(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    consulta_id = db.Column(db.Integer, db.ForeignKey("consulta.id"), nullable = False)
    examen = db.Column(db.Text, nullable = False) 
    diagnostico = db.Column(db.Text, nullable = False)  
    tratamiento = db.Column(db.Text, nullable = False)  
    recomendaciones = db.Column(db.Text, nullable = True)  
    consulta = db.relationship("Consulta", back_populates = "registros")