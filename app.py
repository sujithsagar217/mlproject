from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from pymongo import MongoClient
import joblib
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ MongoDB Local Configuration
client = MongoClient("mongodb://localhost:27017/")
db = client["fitness"]
users_collection = db["users"]
submissions_collection = db["submissions"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ✅ Load ML models and encoders
rf_exercises = joblib.load('C:/Users/mahan/Desktop/project/rf_exercises_model.pkl')
rf_diet = joblib.load('C:/Users/mahan/Desktop/project/rf_diet_model.pkl')
label_encoders = joblib.load('C:/Users/mahan/Desktop/project/label_encoders.pkl')

# ✅ Flask-Login compatible user class
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.password = user_data['password']

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

@app.route('/')
@login_required
def home():
    return render_template('index.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users_collection.find_one({'username': username}):
            flash('Username already exists')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        users_collection.insert_one({'username': username, 'password': hashed_pw})
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = users_collection.find_one({'username': username})

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for('home'))

        flash('Invalid credentials')
    return render_template('login.html')

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

        return render_template('result.html', exercise=exercise_result, diet=diet_result)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
