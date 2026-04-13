from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

db = SQLAlchemy(metadata=metadata)

class Volunteer(db.Model):
    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    profile = db.relationship("Profile", back_populates="volunteer", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile": self.profile.to_dict() if self.profile else None
        }

    def __repr__(self):
        return f"Volunteer(name='{self.name}', email='{self.email}')"
    
class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    phone = db.Column(db.String(20))

    volunteer_id = db.Column(db.Integer, db.ForeignKey("volunteers.id"))
    volunteer = db.relationship("Volunteer", back_populates="profile")

    def to_dict(self):
        return {
            "id": self.id,
            "bio": self.bio,
            "phone": self.phone
        }
    
    def __repr__(self):
        return f"Profile(bio='{self.bio}', phone='{self.phone}')"