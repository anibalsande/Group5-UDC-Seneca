import joblib
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class ModelHandler:
    def __init__(self):
        self.model = LinearRegression()  # Modelo de regresión lineal
        self.coef = None

    def load_model(self, file_path):
        """Upload model from a file (.joblib or .pkl)"""
        try:
            if file_path.endswith('.joblib'):
                self.model_info = joblib.load(file_path)
            elif file_path.endswith('.pkl'):
                with open(file_path, 'rb') as f:
                    self.model_info = pickle.load(f)
            else:
                raise ValueError("Unsupported file format. Use .joblib or .pkl.")
            
            # Restore model for prediction
            if 'coefficients' in self.model_info and 'intercept' in self.model_info:
                self.model.coef_ = self.model_info['coefficients']
                self.model.intercept_ = self.model_info['intercept']

        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")
        
    def train_model(self, data, input_columns, output_column, description):
        """
        Trains the linear regression model and optionally displays the results in a separate window.

        Args:
            show_window (bool, optional): Whether to display the results window. Defaults to True.

        Raises:
            QMessageBox: Displays an error message if there is an issue during model training.
        """
        try:
            self.plot_data = data
            self.input_columns = input_columns
            self.output_column = output_column
            X = data[input_columns].values
            y = data[output_column].values

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train the linear regression model
            self.model.fit(X_train, y_train)

            # Make predictions and calculate error metrics on the test set
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            # Calculate formula
            self.coef = self.model.coef_
            self.intercept = self.model.intercept_
            formula_terms = [f"{self.coef[i]:.4f} * {col}" for i, col in enumerate(self.input_columns)]
            formula = f"{self.output_column} = {self.intercept:.4f} + {' + '.join(formula_terms)}"

            # Determine the warning message and the data for the graph
            if len(self.input_columns) > 1:
                self.warning_text = "The graph is only displayed for simple linear regression."

            plot_data = (X_test[:, 0], y_test, y_pred) if len(self.input_columns) == 1 and X_test.shape[1] == 1 else None

            # Pass metrics, formula, and other data to ResultsWindow
            self.r2 = r2
            self.mse = mse
            self.formula = formula
            self.plot_data = plot_data

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in model creation:\n{str(e)}")


    def save_model(self, file_path, model_info):
        """Save model in an specified format."""
        try:
            if file_path.endswith('.joblib'):
                joblib.dump(model_info, file_path)
            elif file_path.endswith('.pkl'):
                with open(file_path, 'wb') as f:
                    pickle.dump(model_info, f)
            else:
                raise ValueError("Unsupported file format. Use .joblib or .pkl.")
        except Exception as e:
            raise RuntimeError(f"Failed to save model: {str(e)}")
        
    def make_prediction(self, input_values):
        """
        Generate predictions based on input.

        Raises:
            ValueError: If any input field is empty or contains non-numeric values.
            QMessageBox: Displays a warning or error message in case of invalid input or unexpected errors during prediction.
        """
        try:
            # Check if all input fields are filled
            input_values = []
            for col in self.input_columns:
                text = self.input_fields[col].text().strip()
                if not text:  
                    raise ValueError(f"Input for '{col}' is missing.")
                try:
                    input_values.append(float(text)) 
                except ValueError:
                    raise ValueError(f"Input for '{col}' must be a numeric value.")  

            input_array = np.array(input_values).reshape(1, -1)
            prediction = np.dot(input_array, self.coef) + self.intercept
            return prediction
        
        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"Unexpected Error:\n{str(e)}") 

