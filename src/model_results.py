import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import os
import joblib  # Importar joblib para guardar el modelo

class ResultsWindow(QDialog):
    def __init__(self, description, r2, mse, formula, plot_data, coef, intercept, input_columns, output_column, warning_text=""):
        super().__init__()
        self.setWindowTitle("Model Results")
        self.setGeometry(100, 100, 800, 600)
        self.setFont(QFont("Bahnschrift", 12))
        self.input_columns = input_columns
        self.output_column = output_column
        self.description = description
        self.plot_data = plot_data
        self.coef = coef
        self.intercept = intercept
        self.r2 = r2
        self.mse = mse
        self.formula = formula

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.data_group = QGroupBox("Model Metrics:")
        self.data_layout = QVBoxLayout()

        self.description_text = QLabel(f"'{description}'")
        self.description_text.setWordWrap(True)
        self.layout.addWidget(self.description_text)

        metrics_text = (f"Coefficient of determination (R²): {self.r2:.4f}\n"
                        f"Mean Squared Error (MSE): {self.mse:.4f}\n\n"
                        f"Model Formula: {self.formula}")

        self.results_label = QLabel(metrics_text)
        self.results_label.setFont(QFont("Bahnschrift", 12))
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.data_layout.addWidget(self.results_label)  # Cambié self.result_layout por self.layout
        
        self.data_group.setLayout(self.data_layout)
        self.layout.addWidget(self.data_group)

        self.warning_label = QLabel(warning_text) if warning_text else QLabel("")
        if warning_text:
            self.warning_label.setStyleSheet("color: red; padding: 10px;")
            self.layout.addWidget(self.warning_label)

        self.save_button = QPushButton("Save model")
        self.save_button.setFixedHeight(28)
        self.save_button.setStyleSheet(""" 
            QPushButton {
                background-color: #F6BE00; 
                color: #0B1E3E;
                border-radius: 5px;
                font-weight: bold;
                padding-left: 15px;
                padding-right: 15px;
            }
            QPushButton:hover {
                background-color: #0B1E3E;
                color: white;
            }
        """)
        self.save_button.clicked.connect(self.save_model)
        self.layout.addWidget(self.save_button)

        if plot_data is not None:
            self.plot_regression_line(plot_data)

        self.prediction_group = QGroupBox("Make a Prediction")
        self.prediction_layout = QFormLayout()
        self.input_fields = {}

        for col in input_columns:
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Enter value for {col}")
            self.prediction_layout.addRow(f"{col}:", input_field)
            self.input_fields[col] = input_field

        self.predict_button = QPushButton("Realizar Predicción")
        self.predict_button.clicked.connect(self.make_prediction)
        self.prediction_layout.addRow(self.predict_button)

        self.prediction_output = QLabel("")
        self.prediction_layout.addRow("Predicción:", self.prediction_output)

        self.prediction_group.setLayout(self.prediction_layout)
        self.layout.addWidget(self.prediction_group)

        self.setLayout(self.layout)

    def plot_regression_line(self, plot_data):
        X_test, y_test, y_pred = plot_data
        
        # Crear un nuevo widget para el gráfico
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        ax.scatter(X_test, y_test, color="blue", label="Real Data", alpha=0.7)
        ax.plot(X_test, y_pred, color="red", label="Fit Line", linewidth=2)
        ax.set_xlabel("Feature")
        ax.set_ylabel("Target")
        ax.set_title("Linear Regression Plot")
        ax.legend()
        ax.grid(True)  # Añadir rejilla al gráfico

        self.layout.addWidget(canvas)
        canvas.draw()  # Dibuja el gráfico

    def save_model(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Model",
            "",
            "Joblib (*.joblib);;All Files (*)",
            options=QFileDialog.Option.DontConfirmOverwrite
        )
        
        if file_path:
            # Asegurarse de que la extensión sea .joblib
            if not file_path.endswith('.joblib'):
                file_path += '.joblib'

            try:             
                model_info = {
                    'description': self.description_text.text(),
                    'metrics': {
                        'R²': self.r2,
                        'MSE': self.mse,
                    },
                    'formula': self.formula,
                    'coefficients': self.coef,
                    'intercept': self.intercept,
                    'input_columns': self.input_columns,
                    'output_column': self.output_column
                }

                joblib.dump(model_info, file_path)  # Save model using joblib
                QMessageBox.information(self, "Done!", f"Model saved successfully in:\n{file_path}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Model couldn't be saved in:\n{str(e)}")

    def make_prediction(self):
        try:
            # Obtener valores de entrada
            input_values = []
            for col in self.input_columns:
                value = self.input_fields[col].text()
                if value == "":
                    raise ValueError("Please, enter all input values.")
                input_values.append(float(value))

            # Calcular predicción usando el modelo
            input_array = np.array(input_values).reshape(1, -1)
            prediction = np.dot(input_array, self.coef) + self.intercept

            self.prediction_output.setText(f"{prediction[0]:.4f}")
            self.prediction_output.setStyleSheet("color: green; font-weight: bold;")

        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"Unexpected Error:\n{str(e)}")

class ModelTrainer(QWidget):
    def __init__(self, data, input_columns, output_column, description=""):
        super().__init__()
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.description = description
        self.model = LinearRegression()

        self.train_and_show_results()
    
    def train_and_show_results(self, show_window = True):
        try:
            X = self.data[self.input_columns].values
            y = self.data[self.output_column].values

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Entrenar el modelo de regresión lineal
            self.model.fit(X_train, y_train)

            # Realizar predicciones y calcular métricas de error en el conjunto de prueba
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            # Calcular la fórmula del modelo
            self.coef = self.model.coef_
            self.intercept = self.model.intercept_
            formula_terms = [f"{self.coef[i]:.4f} * {col}" for i, col in enumerate(self.input_columns)]
            formula = f"{self.output_column} = {self.intercept:.4f} + {' + '.join(formula_terms)}"

            # Determinar el mensaje de advertencia y los datos de la gráfica
            warning_text = ""
            if len(self.input_columns) > 1:
                warning_text += "Note: The graph is only displayed for a simple linear regression."

            plot_data = (X_test[:, 0], y_test, y_pred) if len(self.input_columns) == 1 and X_test.shape[1] == 1 else None

            # Pasar métricas, fórmula, y otros datos a ResultsWindow
            if show_window:
                results_window = ResultsWindow(self.description, r2, mse, formula, plot_data, self.coef, self.intercept, self.input_columns, self.output_column, warning_text)
                results_window.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en la creación del modelo:\n{str(e)}")
