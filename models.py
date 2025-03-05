import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import CheckConstraint
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("length(username) >= 5 AND length(username) <= 255", name="Users_username_check"),
        CheckConstraint("username ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'", name="Users_username_check1"),
    )


class Workout(db.Model):
    __tablename__ = "Workouts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    workout_name = db.Column(db.String(255), nullable=False)
    body_group = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "workout_name", name="Workouts_user_id_workout_name_key"),
    )


class Exercise(db.Model):
    __tablename__ = "Exercises"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Workouts.id", ondelete="CASCADE"), nullable=False)
    exercise_name = db.Column(db.String(255), nullable=False)
    muscle_group = db.Column(db.String(255), nullable=False)
    num_sets = db.Column(db.Integer)
    num_reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    target_weight = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("workout_id", "exercise_name", name="Exercises_workout_id_exercise_name_key"),
    )
