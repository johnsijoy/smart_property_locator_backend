import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

# Sample training data (you can replace this with real property dataset)
# Features: [area, bhk, age]
X = np.array([
    [1000, 2, 5],
    [1500, 3, 3],
    [2000, 4, 1],
    [1200, 2, 10],
    [1800, 3, 7]
])
# Target (price in $)
y = np.array([50_000, 80_000, 120_000, 55_000, 95_000])

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
save_dir = os.path.join(os.path.dirname(__file__), 'ml_models')
os.makedirs(save_dir, exist_ok=True)
joblib.dump(model, os.path.join(save_dir, 'price_model.pkl'))

print("✅ Model trained and saved to ml_models/price_model.pkl")
