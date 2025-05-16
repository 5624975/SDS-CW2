from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Association Table
task_assignments = db.Table('task_assignments',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    recovery_code = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='member')  # 'manager' or 'member'

    # Backref to access tasks user is assigned to
    assigned_tasks = db.relationship('Task', secondary=task_assignments, back_populates='assigned_users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)

    # Many-to-many relationship
    assigned_users = db.relationship('User', secondary=task_assignments, back_populates='assigned_tasks')
