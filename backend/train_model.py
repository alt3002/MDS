import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import fastparquet
# Define the path to your dataset file (adjust if necessary)
# Here we assume a CSV file with columns F1, F2, ..., F2381 and a 'Label' column




# Define the path to the dataset file
dataset_path = os.path.join(os.getcwd(), 'dataset', 'ember', 'test_ember_2018_v2_features.parquet')

# Load the dataset using pandas (requires pyarrow or fastparquet installed)
try:
    df = pd.read_parquet(dataset_path, engine='fastparquet')
except Exception as e:
    print("Error loading dataset:", e)
    exit(1)

# Separate features and labels
X = df.drop('Label', axis=1).values
y = df['Label'].values

# Feature Scaling: Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Define a Random Forest classifier
rf = RandomForestClassifier(random_state=42)

# Expanded hyperparameter grid for tuning
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2']
}

# Set up GridSearchCV with 5-fold cross-validation
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5,
    n_jobs=-1,
    verbose=2
)

# Fit GridSearchCV on the training data
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
print("Best Hyperparameters:", grid_search.best_params_)

# Evaluate the best model on the test set
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Test Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the scaler and the best model
model_dir = os.path.join(os.getcwd(), 'model')
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, 'malware_detection_model.pkl')
scaler_path = os.path.join(model_dir, 'scaler.pkl')

with open(model_path, 'wb') as f:
    pickle.dump(best_model, f)
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

print("Model and scaler trained and saved successfully at:")
print(model_path)
print(scaler_path)





"""

import pickle
from sklearn.linear_model import LogisticRegression
import numpy as np
import os

# Create dummy data
X = np.random.rand(100, 4)  # 100 samples, 4 features
y = np.random.randint(0, 2, 100)  # Binary labels: 0 (benign) or 1 (malicious)

# Train a Logistic Regression model
model = LogisticRegression()
model.fit(X, y)

# Ensure the model directory exists
model_dir = os.path.join(os.getcwd(), 'model')
os.makedirs(model_dir, exist_ok=True)

# Save the model using pickle
model_path = os.path.join(model_dir, 'malware_detection_model_0.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print("Dummy model trained and saved successfully at:", model_path)
"""


