import os
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from feature_extractor import extract_features
from predictor import predict_file  # [MODIFIED: Added predictor import]

app = Flask(__name__)
CORS(app)

# Define the model path (ensure this path is correct relative to backend/)
# ... (existing imports and code)

# Load the model as before
MODEL_PATH = os.path.join(os.getcwd(), 'model', 'malware_detection_model.pkl')

if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully.")
    except Exception as e:
        print("Error loading model:", e)
        model = None
else:
    model = None
    print("Model file not found. Please train and save your model as 'malware_detection_model.pkl' in the 'model' folder.")

# --- Add the scaler loading code here ---
SCALER_PATH = os.path.join(os.getcwd(), 'model', 'scaler.pkl')

if os.path.exists(SCALER_PATH):
    try:
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        print("Scaler loaded successfully.")
    except Exception as e:
        print("Error loading scaler:", e)
        scaler = None
else:
    scaler = None
    print("Scaler file not found. Please train and save your scaler in the 'model' folder.")

# ... (rest of your code remains unchanged)

@app.route('/scan', methods=['POST'])
def scan_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    os.makedirs('uploads', exist_ok=True)
    file_path = os.path.join(os.getcwd(), 'uploads', file.filename)
    file.save(file_path)

    # [MODIFIED] Instead of manually extracting/scaling/predicting,
    # use the predictor function to get the result.
    result = predict_file(file_path)

    # [REMOVED] The manual extraction and prediction code is now replaced.
    # features = extract_features(file_path)
    # if scaler is not None:
    #     features = scaler.transform([features])[0]
    # if model is None:
    #     result = "Model not available"
    # else:
    #     prediction = model.predict([features])[0]
    #     result = "Malicious" if prediction == 1 else "Benign"

    os.remove(file_path)

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
