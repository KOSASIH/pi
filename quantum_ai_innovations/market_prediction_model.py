import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

class MarketPredictionModel:
    def __init__(self, data_file):
        self.data_file = data_file
        self.model = LinearRegression()
        self.history = None

    def load_data(self):
        # Load historical price data from a CSV file
        self.history = pd.read_csv(self.data_file)
        print("Data loaded successfully.")
        print(self.history.head())

    def preprocess_data(self):
        # Prepare the data for training
        # Assuming the CSV has columns 'Date' and 'Price'
        self.history['Date'] = pd.to_datetime(self.history['Date'])
        self.history['Date'] = self.history['Date'].map(pd.Timestamp.timestamp)  # Convert to timestamp

        # Features and target variable
        X = self.history[['Date']]  # Features (independent variable)
        y = self.history['Price']    # Target (dependent variable)

        return X, y

    def train_model(self):
        X, y = self.preprocess_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        self.model.fit(X_train, y_train)
        print("Model trained successfully.")

        # Evaluate the model
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f"Mean Squared Error: {mse:.2f}")

        # Plotting the results
        plt.scatter(X_test, y_test, color='blue', label='Actual Prices')
        plt.scatter(X_test, predictions, color='red', label='Predicted Prices')
        plt.xlabel('Date (timestamp)')
        plt.ylabel('Price')
        plt.title('Market Price Prediction')
        plt.legend()
        plt.show()

    def predict_price(self, date):
        # Predict the price for a given date
        timestamp = pd.Timestamp(date).timestamp()
        predicted_price = self.model.predict(np.array([[timestamp]]))
        return predicted_price[0]

if __name__ == "__main__":
    # Example usage
    model = MarketPredictionModel(data_file='historical_prices.csv')  # Replace with your CSV file path
    model.load_data()
    model.train_model()

    # Predicting the price for a specific date
    date_to_predict = '2023-12-31'  # Example date
    predicted_price = model.predict_price(date_to_predict)
    print(f"Predicted price for {date_to_predict}: ${predicted_price:.2f}")
