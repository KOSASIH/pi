# decentralized_ai_service.py

import numpy as np
from sklearn.linear_model import LinearRegression
import json

class DecentralizedAIService:
    def __init__(self):
        self.models = {}

    def train_model(self, model_id, features, targets):
        # Train a linear regression model
        X = np.array(features).reshape(-1, 1)
        y = np.array(targets)
        model = LinearRegression()
        model.fit(X, y)
        self.models[model_id] = model
        print(f"Model {model_id} trained.")

    def predict(self, model_id, new_data):
        # Make predictions using the trained model
        if model_id in self.models:
            model = self.models[model_id]
            prediction = model.predict(np.array(new_data).reshape(-1, 1))
            return prediction.tolist()
        else:
            raise ValueError("Model not found.")

if __name__ == "__main__":
    # Example usage
    service = DecentralizedAIService()
    service.train_model("model 1", [1, 2, 3, 4, 5], [2, 3, 5, 7, 11])
    predictions = service.predict("model1", [6, 7, 8])
    print("Predictions for new data:", predictions)
