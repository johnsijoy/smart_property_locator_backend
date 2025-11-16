import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import pickle

# Base directory (current folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Step 1: Load CSV
csv_path = os.path.join(BASE_DIR, "property_data.csv")
data = pd.read_csv(csv_path)

# Step 2: Split features and target
X = data[["location", "property_type", "bhk", "area_sqft"]]
y = data["price"]

# Step 3: Preprocess categorical data
categorical_features = ["location", "property_type"]
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
    remainder='passthrough'
)

X_transformed = preprocessor.fit_transform(X)

# Step 4: Train Linear Regression model
model = LinearRegression()
model.fit(X_transformed, y)

# Step 5: Save the encoder and model in prediction/ folder
encoder_path = os.path.join(BASE_DIR, "encoder.pkl")
model_path = os.path.join(BASE_DIR, "model.pkl")

with open(encoder_path, "wb") as f:
    pickle.dump(preprocessor, f)

with open(model_path, "wb") as f:
    pickle.dump(model, f)

print("Training complete. Encoder and model saved!")
