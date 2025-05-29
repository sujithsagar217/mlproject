import joblib

# Base directory inside the container
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model using relative path
rf_exercises = joblib.load(os.path.join(BASE_DIR, 'rf_exercises_model.pkl'))
rf_diet = joblib.load(os.path.join(BASE_DIR, 'rf_diet_model.pkl'))
label_encoders = joblib.load(os.path.join(BASE_DIR, 'label_encoders.pkl'))

def predict_exercise_and_diet(features):
    # Predict class labels
    exercise_pred = rf_exercises.predict([features])[0]
    diet_pred = rf_diet.predict([features])[0]

    # Decode to string labels
    exercise_label = label_encoders['Exercises'].inverse_transform([exercise_pred])[0]
    diet_label = label_encoders['Diet'].inverse_transform([diet_pred])[0]

    return exercise_label, diet_label


