import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def train_and_save_model():
    data = pd.DataFrame({
        'location': ['Pleasantville', 'Greenville', 'Pleasantville', 'Greenville', 'Sunnyvale'],
        'property_type': ['Apartment', 'Villa', 'Villa', 'Apartment', 'Apartment'],
        'bhk': [2, 3, 4, 2, 3],
        'area': [1000, 1500, 2000, 1200, 1800],
        'price': [50000, 80000, 120000, 60000, 90000]
    })

    X = data[['location', 'property_type', 'bhk', 'area']]
    y = data['price']

    categorical_features = ['location', 'property_type']

    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(), categorical_features)],
        remainder='passthrough'
    )

    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    model_pipeline.fit(X, y)
    joblib.dump(model_pipeline, 'prediction/property_price_model.pkl')

if __name__ == '__main__':
    train_and_save_model()
