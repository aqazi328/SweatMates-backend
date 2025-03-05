from flask import Flask, request, jsonify
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import bcrypt
import jwt
import datetime
from models import db, User, Workout, Exercise

# Define variables
app = Flask(__name__)
load_dotenv()
hostname = os.getenv("HOSTNAME")
db_name = os.getenv("DATABASE")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
port_ID = os.getenv("PORT_ID")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRATION_SECONDS = int(os.getenv("JWT_EXPIRATION_SECONDS", 3600))

# Database config and migration setup
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", f"postgresql://{db_username}:{db_password}@{hostname}:{port_ID}/{db_name}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)

# Authentication Functions
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION_SECONDS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def decode_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        token = token.split("Bearer ")[-1]
        decoded = decode_jwt(token)
        if not decoded:
            return jsonify({"message": "Invalid or expired token!"}), 401
        return f(decoded["user_id"], *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# ROUTES
@app.get("/")
def home():
    return "Hello Sweatmate!"

@app.post("/signup")
def signup_in():
    data = request.get_json()
    input_username = data["username"]
    input_password = data["password"]

    try:
        new_user = User(username=input_username, password_hash=hash_password(input_password))
        db.session.add(new_user)
        db.session.commit()
        token = generate_jwt(str(new_user.id))
        return {"id": str(new_user.id), "token": token, "message": "User created successfully"}, 201
    except Exception as e:
        return {"id": None, "message": str(e)}, 400

@app.post("/login")
def log_in():
    data = request.get_json()
    input_username = data["username"]
    input_password = data["password"]
   
    user = User.query.filter_by(username=input_username).first()
    if user and check_password(input_password, user.password_hash):
        token = generate_jwt(str(user.id))
        return {"id": str(user.id), "token": token,"message": "Login successful"}, 200
    return {"message": "Invalid credentials"}, 401
    
@app.post("/addworkout")
@token_required
def add_workout(user_id):
    data = request.get_json()
    workout_name = data["workoutName"]
    body_group = data["bodyGroup"]
    notes = data["notes"]

    try:
        new_workout = Workout(user_id=user_id, workout_name=workout_name, body_group=body_group, notes=notes)
        db.session.add(new_workout)
        db.session.commit()
        return {"id": str(new_workout.id), "message": "Workout added successfully"}, 201
    except Exception as e:
        return {"message": str(e)}, 400
    

if __name__ == "__main__":
    app.run(debug=True)