from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

db = SQLAlchemy(metadata=metadata)

class Volunteer(db.Model, SerializerMixin):
    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    profile = db.relationship("Profile", back_populates="volunteer", uselist=False, cascade="all, delete-orphan")

    task_assignments = db.relationship("TaskAssignment",back_populates="volunteer", cascade="all, delete-orphan")

    serialize_rules = ('-profile.volunteer', '-task_assignments.volunteer', '-task_assignments.task.task_assignments')

    def __repr__(self):
        return f"Volunteer(name='{self.name}', email='{self.email}')"
    
class Profile(db.Model, SerializerMixin):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    phone = db.Column(db.String(20))
    volunteer_id = db.Column(db.Integer, db.ForeignKey("volunteers.id"))

    volunteer = db.relationship("Volunteer", back_populates="profile")

    serialize_rules =('-volunteer.profile',)
    
    def __repr__(self):
        return f"Profile(bio='{self.bio}', phone='{self.phone}')"
    
class Project(db.Model, SerializerMixin):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

    tasks = db.relationship("Task", back_populates="project", cascade="all, delete-orphan")

    serialize_rules = ('-tasks.project',)

    def __repr__(self):
        return f"Project(name='{self.name}', description='{self.description}')"

class Task(db.Model, SerializerMixin):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    project = db.relationship("Project", back_populates="tasks")
    
    # Many-to-many Relationship with Tasks
    task_assignments = db.relationship("TaskAssignment",back_populates="task", cascade="all, delete-orphan")

    serialize_rules = ('-project.tasks', '-task_assignment.task', '-task_assignments.volunteer.task_assignments')

    def __repr__(self):
        return f"Task(title='{self.title}', description='{self.description}')"

class TaskAssignment(db.Model, SerializerMixin):
    __tablename__ = "task_assignment"

    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey("volunteers.id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))

    volunteer = db.relationship("Volunteer",back_populates="task_assignments")
    task = db.relationship("Task",back_populates="task_assignments")

    serialize_rules = ('-volunteer.task_assignments','-task.task_assignments')