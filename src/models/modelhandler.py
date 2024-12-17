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
        self.plot_data = None
        self.intercept = None
        self.description = None
        self.metrics = {}
        self.formula = None
        self.input_columns = None
        self.output_column = None

    def load_model(self, file_path):
        """Upload model from a file (.joblib or .pkl)"""
        try:
            if file_path.endswith('.joblib'):
                loaded_data = joblib.load(file_path)
            elif file_path.endswith('.pkl'):
                with open(file_path, 'rb') as f:
                    loaded_data = pickle.load(f)
            else:
                raise ValueError("Unsupported file format. Use .joblib or .pkl.")

            # Asignar variables
            self.coef = loaded_data['coefficients']
            self.intercept = loaded_data['intercept']
            self.description = loaded_data['description']
            self.metrics = loaded_data['metrics']
            self.formula = loaded_data['formula']
            self.input_columns = loaded_data['input_columns']
            self.output_column = loaded_data['output_column']

        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")
        
    def train_model(self, data, input_columns, output_column, description = "No description provided"):
        """
        Trains the linear regression model and optionally displays the results in a separate window.

        Args:
            show_window (bool, optional): Whether to display the results window. Defaults to True.

        Raises:
            QMessageBox: Displays an error message if there is an issue during model training.
        """
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
        self.input_columns = input_columns
        self.output_column = output_column
        self.description = description
        self.metrics = {'R²': r2, 'MSE': mse}

        self.plot_data = (X_test[:, 0], y_test, y_pred) if len(self.input_columns) == 1 and X_test.shape[1] == 1 else None

        formula_terms = [f"{self.coef[i]:.4f} * {col}" for i, col in enumerate(input_columns)]
        self.formula = f"{output_column} = {self.intercept:.4f} + {' + '.join(formula_terms)}"

    def save_model(self, file_path):
        """
        Save model to a .joblib file. The method opens a file dialog for the user to specify the file path where the model
        will be saved.

        Raises:
            QMessageBox: Displays an error message if the model cannot be saved due to any issue.
        """
        try:
            model_info = {
                'description': self.description,
                'metrics': {
                    'R²': self.metrics['R²'],
                    'MSE': self.metrics['MSE'],
                },
                'formula': self.formula,
                'coefficients': self.coef,
                'intercept': self.intercept,
                'input_columns': self.input_columns,
                'output_column': self.output_column,
            }
            if file_path.endswith('.joblib'):
                joblib.dump(model_info, file_path)
            elif file_path.endswith('.pkl'):
                with open(file_path, 'wb') as f:
                    pickle.dump(model_info, f)
            else:
                return False, "Unsupported file format. Use .joblib or .pkl."
            return True, f"Model saved successfully in:\n{file_path}"
        except Exception as e:
            return False, f"Model couldn't be saved:\n{str(e)}"

    def make_prediction(self, input_fields):
        """
        Generate predictions based on input.

        Raises:
            ValueError: If any input field is empty or contains non-numeric values.
        """
        input_values = []
        for col in self.input_columns:
            text = input_fields[col].text().strip()
            if not text:  
                raise ValueError(f"Input for '{col}' is missing.")
            try:
                input_values.append(float(text)) 
            except ValueError:
                raise ValueError(f"Input for '{col}' must be a numeric value.")  

        input_array = np.array(input_values).reshape(1, -1)
        prediction = np.dot(input_array, self.coef) + self.intercept
        return prediction