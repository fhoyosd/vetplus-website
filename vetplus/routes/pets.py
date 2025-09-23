from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from vetplus.models import Pet, User
from vetplus.utils import admin_required
from vetplus.extensions import db

pets_bp = Blueprint("pets", __name__)

@pets_bp.route("/pets")
@login_required
def pet_list():
    if current_user.role == "owner":
        pets = Pet.query.filter_by(owner_id = current_user.id).all()

        return render_template("pets/manage_pets.html", pets = pets)
    else:
        return "Acceso no autorizado", 403

# @pets_bp.route("/pets/manage", methods=["GET", "POST"])
# @login_required
# def manage_pets():
#     if request.method == "POST":
#         try:
#             # Datos del formulario
#             name = request.form.get("name")
#             species = request.form.get("species")
#             breed = request.form.get("breed")
#             age = request.form.get("age", type=int)
#             weight = request.form.get("weight", type=float)
#             owner_id = request.form.get("owner_id", type=int)

#             new_pet = Pet(
#                 name = name,
#                 species = species,
#                 breed = breed,
#                 age = age,
#                 weight = weight,
#                 owner_id = owner_id
#             )

#             db.session.add(new_pet)
#             db.session.commit()

#             flash("Mascota registrada con éxito ✅", "success")
#             return redirect(url_for("pets.manage_pets"))

#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error al registrar mascota ❌: {str(e)}", "danger")
#             return redirect(url_for("pets.manage_pets"))

#     pets = Pet.query.all()
#     owners = User.query.filter_by(role = "owner").all()
#     vets = User.query.filter_by(role = "vet").all()

#     return render_template(
#         "admin/pets/manage_pets.html",
#         pets = pets,
#         owners = owners,
#         vets = vets
#     )

    
@pets_bp.route("/pets/add", methods = ["POST"])
@login_required
def add_pet():
    if current_user.role != "owner" and current_user.role != "vet":
        return "Acceso no autorizado", 403

    name = request.form.get("name")
    species = request.form.get("species")
    breed = request.form.get("breed")
    age = request.form.get("age")
    weight = request.form.get("weight")

    new_pet = Pet(name = name, species = species, breed = breed, age = age, owner_id = current_user.id, weight = weight)
    db.session.add(new_pet)
    db.session.commit()

    return redirect(url_for("pets.pet_list"))

@pets_bp.route("/pets/edit/<int:pet_id>", methods = ["GET", "POST"])
@login_required
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)

    if current_user.role == "owner" and pet.owner_id != current_user.id:
        return "Acceso no autorizado", 403
    elif current_user.role == "vet" and current_user not in pet.veterinarians:
        return "Acceso no autorizado", 403

    if request.method == "POST":
        pet.name = request.form.get("name")
        pet.species = request.form.get("species")
        pet.breed = request.form.get("breed")
        pet.age = request.form.get("age")

        db.session.commit()
        return redirect(url_for("pets.pet_list"))

    return render_template("pets/edit_pet.html", pet = pet)

@pets_bp.route("/pets/delete/<int:pet_id>")
@login_required
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)

    if current_user.role == "owner" and pet.owner_id != current_user.id:
        return "Acceso no autorizado", 403
    elif current_user.role == "vet" and current_user not in pet.veterinarians:
        return "Acceso no autorizado", 403

    db.session.delete(pet)
    db.session.commit()

    return redirect(url_for("pets.pet_list"))