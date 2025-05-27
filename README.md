# 🏋️‍♂️ Health and Fitness Recommendation System

This is a Flask-based web application that helps users get personalized health recommendations — including both exercise and diet suggestions — based on their physical profile and fitness goals. It uses trained machine learning models to provide these recommendations.

---

## 📌 What This App Does

* Allows users to register/login securely.
* Collects user input (age, weight, height, BMI, etc.).
* Predicts best-fit **exercise** and **diet** using ML models.
* Stores each submission securely in a MongoDB collection.
* Displays historical recommendations to users.

---

## 🧰 Technical Stack

### 🔙 Backend

* **Flask**: Lightweight Python web framework.
* **Flask-Login**: Session management and user authentication.
* **Werkzeug Security**: Password hashing & verification.
* **PyMongo**: Interface between Flask and MongoDB.
* **Joblib**: Used to load pre-trained ML models and encoders.
* **scikit-learn**: Library used to train models (not needed at runtime).

### 🧠 ML Models

* Models are trained separately using scikit-learn and saved using `joblib`.
* Two models used:

  * `rf_exercises_model.pkl`: Predicts the recommended exercise.
  * `rf_diet_model.pkl`: Predicts the appropriate diet.
* `label_encoders.pkl` contains encoders for categorical fields.

### 💾 Database

* **MongoDB** (running locally on `localhost:27017`):

  * Database name: `fitness`
  * Collections:

    * `users`: Stores registered users.
    * `submissions`: Stores user inputs and model predictions.

---

## ✅ Best Practices Followed

* Passwords hashed before storing in DB using `generate_password_hash`.
* Authenticated routes protected with `@login_required`.
* Flash messages used for feedback.
* Bootstrap + custom styling for responsive UI.
* Consistent design and validation across templates.

---

## 🖥️ Running Locally on Windows

### 🔧 One-Time Setup

#### 1. ✅ Install MongoDB Community Edition

* Download from: [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
* During setup, ensure to:

  * Choose **Complete** installation
  * Check **"Install MongoDB as a Service"** (this allows auto-start)

#### 2. ✅ Create Virtual Environment & Activate It

```bash
cd path\to\your\project
python -m venv venv
venv\Scripts\activate
```

#### 3. ✅ Generate and Install Python Dependencies

To create your `requirements.txt` file (only once):

```bash
pip3 freeze > requirements.txt
```

To install dependencies (for new users):

```bash
pip install -r requirements.txt
```

#### 4. ✅ Ensure You Have Model Files

Ensure these files exist:

```
rf_exercises_model.pkl
rf_diet_model.pkl
label_encoders.pkl
```

Path in `app.py`:

```python
joblib.load(r'C:\Users\HP\Desktop\mlproject\rf_exercises_model.pkl')
```

Adjust path if necessary.

#### 5. ✅ MongoDB Service Should Be Running

MongoDB starts automatically as a service after install. If not:

```bash
net start MongoDB
```

#### 6. ✅ MongoDB Database Auto-Creation

The app will automatically create the `fitness` database and collections (`users`, `submissions`) on first insert. No manual setup needed.

---

### 🚀 Running the App (Each Time)

```bash
cd path\to\your\project
venv\Scripts\activate
python app.py
```

Open your browser at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📂 File Structure

```
project/
├── app.py
├── models/
│   ├── rf_exercises_model.pkl
│   ├── rf_diet_model.pkl
│   └── label_encoders.pkl
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── result.html
│   ├── error.html
│   └── submissions.html
├── static/
│   └── css/
│       └── style.css
├── requirements.txt
└── README.md
```

---

## 🤝 Contributions & Feedback

If you’d like to improve this project or have feedback, feel free to fork it or message the author.

---

Built with ❤️ using Python, Flask & ML.
