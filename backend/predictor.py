import os
import pickle
from feature_extractor import extract_features

# Load model and scaler (ensure these paths are correct)
MODEL_PATH = os.path.join(os.getcwd(), 'model', 'malware_detection_model.pkl')
SCALER_PATH = os.path.join(os.getcwd(), 'model', 'scaler.pkl')

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

def predict_file(file_path):
    """
    Given a file path, extracts features, scales them, and predicts using the loaded model.
    Returns the prediction ("Malicious" or "Benign").
    """
    features = extract_features(file_path)
    # Scale features: transform expects a 2D array
    scaled_features = scaler.transform([features])[0]
    prediction = model.predict([scaled_features])[0]
    return "Malicious" if prediction == 1 else "Benign"
