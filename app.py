from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import joblib
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# MongoDB Configuration
mongo_uri = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(mongo_uri)
db = client["fitness"]
users_collection = db["users"]
submissions_collection = db["submissions"]

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load ML models and encoders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
rf_exercises = joblib.load(os.path.join(BASE_DIR, 'rf_exercises_model.pkl'))
rf_diet = joblib.load(os.path.join(BASE_DIR, 'rf_diet_model.pkl'))
label_encoders = joblib.load(os.path.join(BASE_DIR, 'label_encoders.pkl'))

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data.get('email')
        self.password = user_data['password']

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    return User(user_data) if user_data else None

@app.route('/')
@login_required
def home():
    return render_template('index.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if users_collection.find_one({'email': email}):
            flash('Email already registered.')
            return redirect(url_for('register'))

        if users_collection.find_one({'username': username}):
            flash('Username already exists.')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': hashed_pw
        })

        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username']
        password = request.form['password']

        user_data = users_collection.find_one({
            '$or': [{'username': username_or_email}, {'email': username_or_email}]
        })

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for('home'))

        flash('Invalid credentials')
    return render_template('login.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        raw_inputs = {
            'Sex': request.form['Sex'],
            'Age': int(request.form['Age']),
            'Height': float(request.form['Height']),
            'Weight': float(request.form['Weight']),
            'BMI': float(request.form['BMI']),
            'Hypertension': request.form['Hypertension'],
            'Diabetes': request.form['Diabetes'],
            'Level': request.form['Level'],
            'Fitness Goal': request.form['Fitness Goal'],
            'Fitness Type': request.form['Fitness Type']
        }

        encoded_inputs = [
            label_encoders['Sex'].transform([raw_inputs['Sex']])[0],
            raw_inputs['Age'],
            raw_inputs['Height'],
            raw_inputs['Weight'],
            raw_inputs['BMI'],
            label_encoders['Hypertension'].transform([raw_inputs['Hypertension']])[0],
            label_encoders['Diabetes'].transform([raw_inputs['Diabetes']])[0],
            label_encoders['Level'].transform([raw_inputs['Level']])[0],
            label_encoders['Fitness Goal'].transform([raw_inputs['Fitness Goal']])[0],
            label_encoders['Fitness Type'].transform([raw_inputs['Fitness Type']])[0]
        ]

        exercise_pred = rf_exercises.predict([encoded_inputs])[0]
        diet_pred = rf_diet.predict([encoded_inputs])[0]

        exercise_result = label_encoders['Exercises'].classes_[exercise_pred]
        diet_result = label_encoders['Diet'].classes_[diet_pred]

        submission = {
            'user_id': ObjectId(current_user.id),
            'sex': raw_inputs['Sex'],
            'age': raw_inputs['Age'],
            'height': raw_inputs['Height'],
            'weight': raw_inputs['Weight'],
            'bmi': raw_inputs['BMI'],
            'hypertension': raw_inputs['Hypertension'],
            'diabetes': raw_inputs['Diabetes'],
            'level': raw_inputs['Level'],
            'fitness_goal': raw_inputs['Fitness Goal'],
            'fitness_type': raw_inputs['Fitness Type'],
            'exercise': exercise_result,
            'diet': diet_result
        }
        submissions_collection.insert_one(submission)

        return render_template('result.html', exercise=exercise_result, diet=diet_result, user=current_user)
    except Exception as e:
        return render_template('error.html', error=str(e), user=current_user)

@app.route('/dashboard')
@login_required
def dashboard():
    cursor = submissions_collection.find({'user_id': ObjectId(current_user.id)}).sort('_id', 1)
    records = []
    for r in cursor:
        r['_id'] = str(r['_id'])
        r['user_id'] = str(r['user_id'])
        r['timestamp'] = ObjectId(str(r['_id'])).generation_time.isoformat()
        records.append(r)

    return render_template('dashboard.html', user=current_user, records=records)

@app.route('/history')
@login_required
def history():
    user_history_cursor = submissions_collection.find({'user_id': ObjectId(current_user.id)}).sort('_id', -1)
    user_history = list(user_history_cursor)
    return render_template('history.html', records=user_history, user=current_user)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
