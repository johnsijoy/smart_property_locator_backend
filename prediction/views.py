import os
import pickle
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the pre-trained model and encoder
with open(os.path.join(BASE_DIR, "prediction", "encoder.pkl"), "rb") as f:
    preprocessor = pickle.load(f)

with open(os.path.join(BASE_DIR, "prediction", "model.pkl"), "rb") as f:
    model = pickle.load(f)


@csrf_exempt  # Allows POST from React frontend without CSRF token
def predict_price(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from frontend
            # Convert dict to DataFrame
            df = pd.DataFrame([{
                "location": data.get("location"),
                "property_type": data.get("property_type"),
                "bhk": int(data.get("bhk")),
                "area_sqft": float(data.get("area_sqft"))
            }])

            # Transform and predict
            X_transformed = preprocessor.transform(df)
            prediction = model.predict(X_transformed)

            return JsonResponse({"predicted_price": round(prediction[0], 2)})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method is allowed."}, status=400)
