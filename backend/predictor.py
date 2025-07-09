from feature_extractor import extract_features

def predict_file(file_path, model, scaler):
    """
    Given a file path, extracts features, scales them, and predicts using the provided model and scaler.
    Returns the prediction ("Malicious" or "Benign").
    """
    features = extract_features(file_path)
    scaled_features = scaler.transform([features])[0]
    prediction = model.predict([scaled_features])[0]
    return "Malicious" if prediction == 1 else "Benign"
