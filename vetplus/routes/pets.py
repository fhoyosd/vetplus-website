from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from vetplus.models import Pet
from vetplus.extensions import db

pets_bp = Blueprint("pets", __name__)

@pets_bp.route("/pets")
@login_required
def pet_list():
    if current_user.role == "owner":
        pets = Pet.query.filter_by(owner_id = current_user.id).all()

        return render_template("pets/owner_pet_list.html", pets = pets)
    elif current_user.role == "vet":
        pets = current_user.patients

        return render_template("pets/vet_pet_list.html", pets = pets)
    else:
        return "Acceso no autorizado", 403
    
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