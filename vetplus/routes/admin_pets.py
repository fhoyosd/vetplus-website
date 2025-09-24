from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from vetplus.models import Pet, User
from vetplus.extensions import db
from vetplus.utils import admin_required

admin_pets_bp = Blueprint("admin_pets", __name__)

@admin_pets_bp.route("/admin/pets/manage", methods = ["GET", "POST"])
@login_required
def manage_pets():
    admin_required()
    if request.method == "POST":
        name = request.form.get("name")
        species = request.form.get("species")
        breed = request.form.get("breed")
        age = request.form.get("age", type = int)
        weight = request.form.get("weight", type = float)
        owner_id = request.form.get("owner_id", type = int)

        new_pet = Pet(
            name = name,
            species = species,
            breed = breed,
            age = age,
            weight = weight,
            owner_id = owner_id,
        )
        db.session.add(new_pet)
        db.session.commit()
        flash("Mascota registrada correctamente ✅", "success")
        return redirect(url_for("admin_pets.manage_pets"))

    pets = Pet.query.all()
    owners = User.query.filter_by(role = "owner").all()
    vets = User.query.filter_by(role = "vet").all()
    return render_template("admin/pets/manage_pets.html", pets = pets, owners = owners, vets = vets)

@admin_pets_bp.route("/admin/pets/edit/<int:pet_id>", methods=["GET", "POST"])
@login_required
def edit_pet(pet_id):
    admin_required()
    pet = Pet.query.get_or_404(pet_id)

    if request.method == "POST":
        pet.name = request.form.get("name")
        pet.species = request.form.get("species")
        pet.breed = request.form.get("breed")
        pet.age = request.form.get("age", type = int)
        pet.weight = request.form.get("weight", type = float)
        pet.owner_id = request.form.get("owner_id", type = int)
        pet.vet_id = request.form.get("vet_id", type = int)

        db.session.commit()
        flash("Mascota actualizada correctamente.", "success")
        return redirect(url_for("admin_pets.manage_pets"))

    owners = User.query.filter_by(role="owner").all()
    vets = User.query.filter_by(role="vet").all()
    return render_template("admin/pets/edit_pet.html", pet = pet, owners = owners, vets = vets)

@admin_pets_bp.route("/admin/pets/delete/<int:pet_id>")
@login_required
def delete_pet(pet_id):
    admin_required()
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash("Mascota eliminada correctamente 🗑", "success")
    return redirect(url_for("admin_pets.manage_pets"))
