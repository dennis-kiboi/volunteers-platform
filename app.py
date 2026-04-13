from flask import Flask, request, jsonify
from models import db, Volunteer, Profile
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/", methods=["GET"])
def home():
    return {"message": "Welcome to the Volunteer Platform API"}

# /volunteers CRUD

# Create a new volunteer


@app.route("/volunteers", methods=["POST"])
def create_volunteer():
    data = request.get_json()
    new_volunteer = Volunteer(name=data["name"], email=data["email"])

    try:
        db.session.add(new_volunteer)
        db.session.commit()
        return new_volunteer.to_dict(), 201
    except Exception:
        db.session.rollback()
        return {"message": "An error occurred while creating the volunteer"}, 500

# Get all volunteers


@app.route("/volunteers", methods=["GET"])
def get_volunteers():
    volunteers = Volunteer.query.all()
    return jsonify(volunteers=[volunteer.to_dict() for volunteer in volunteers])

# Get a specific volunteer by ID


@app.route("/volunteers/<int:volunteer_id>", methods=["GET"])
def get_volunteer(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    return jsonify(volunteer.to_dict())

# Update a volunteer


@app.route("/volunteers/<int:volunteer_id>", methods=["PATCH"])
def update_volunteer(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    data = request.get_json()

    if not data:
        return {"message": "No data provided"}, 400

    try:
        if "name" in data:
            volunteer.name = data["name"]
        if "email" in data:
            volunteer.email = data["email"]

        db.session.commit()
        return jsonify(volunteer.to_dict()), 200
    except Exception:
        db.session.rollback()
        return {"message": "An error occurred while updating the volunteer"}, 500

# Delete a volunteer


@app.route("/volunteers/<int:volunteer_id>", methods=["DELETE"])
def delete_volunteer(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)

    if not volunteer:
        return {"message": "Volunteer not found"}, 404

    try:
        db.session.delete(volunteer)
        db.session.commit()
        return jsonify({}), 204
    except Exception:
        db.session.rollback()
        return {"message": "An error occurred while deleting the volunteer"}, 500

# /profiles CRUD
# Create a new profile for a volunteer


@app.route("/profiles", methods=["POST"])
def create_profile():
    data = request.get_json()
    volunteer_id = data.get("volunteer_id")

    if not volunteer_id:
        return {"message": "Volunteer ID is required"}, 400

    volunteer = Volunteer.query.get(volunteer_id)
    if not volunteer:
        return {"message": "Volunteer not found"}, 404

    new_profile = Profile(
        bio=data["bio"], phone=data["phone"], volunteer=volunteer)

    try:
        db.session.add(new_profile)
        db.session.commit()
        return new_profile.to_dict(), 201
    except Exception:
        db.session.rollback()
        return {"message": "An error occurred while creating the profile"}, 500

# Get all profiles


@app.route("/profiles", methods=["GET"])
def get_profiles():
    profiles = Profile.query.all()
    return jsonify(profiles=[profile.to_dict() for profile in profiles])

# Get a specific profile by ID


@app.route("/profiles/<int:profile_id>", methods=["GET"])
def get_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    return jsonify(profile.to_dict())

# Update a profile


@app.route("/profiles/<int:profile_id>", methods=["PATCH"])
def update_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    data = request.get_json()

    if not data:
        return {"message": "No data provided"}, 400

    try:
        if "bio" in data:
            profile.bio = data["bio"]
        if "phone" in data:
            profile.phone = data["phone"]

        db.session.commit()
        return jsonify(profile.to_dict()), 200
    except Exception:
        db.session.rollback()
        return {"message": "An error occurred while updating the profile"}, 500

# Delete a profile


@app.route("/profiles/<int:profile_id>", methods=["DELETE"])
def delete_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)

    if not profile:
        return {"message": "Profile not found"}, 404

    try:
        db.session.delete(profile)
        db.session.commit()
        return jsonify({}), 204
    except Exception:
        db.session.rollback()
        return {"message": "An error occurred while deleting the profile"}, 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
