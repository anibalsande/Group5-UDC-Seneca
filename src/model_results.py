import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import os
import joblib  # Importar joblib para guardar el modelo

class ResultsWindow(QDialog):
    def __init__(self, description, metrics_text, plot_data, model, input_columns, output_column, warning_text=""):
        super().__init__()
        self.setWindowTitle("Resultados del Modelo")
        self.setGeometry(100, 100, 800, 600)
        self.setFont(QFont("Bahnschrift", 12))
        self.input_columns = input_columns
        self.output_column = output_column
        self.description = description
        self.plot_data = plot_data
        self.metrics_text = metrics_text

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title_label = QLabel("Resultados del Modelo")
        self.title_label.setFont(QFont("Bahnschrift", 16, QFont.Weight.Bold))
        self.layout.addWidget(self.title_label)

        self.description_text = QLabel(description)
        self.description_text.setWordWrap(True)
        self.layout.addWidget(self.description_text)

        # Show metrics in a more robust way
        metrics_lines = metrics_text.split('\n')
        self.results_label = QLabel(metrics_text)
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet("background-color: #E8F0FE; padding: 10px; border-radius: 5px;")
        self.layout.addWidget(self.results_label)

        self.warning_label = QLabel(warning_text) if warning_text else QLabel("")
        if warning_text:
            self.warning_label.setStyleSheet("color: red; padding: 10px;")
            self.layout.addWidget(self.warning_label)

        self.save_button = QPushButton("Guardar Modelo")
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

        self.model = model  # Store the model

        self.setLayout(self.layout)

    def plot_regression_line(self, plot_data):
        X_test, y_test, y_pred = plot_data
        
        # Crear un nuevo widget para el gráfico
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        ax.scatter(X_test, y_test, color="blue", label="Datos reales", alpha=0.7)
        ax.plot(X_test, y_pred, color="red", label="Recta de ajuste", linewidth=2)
        ax.set_xlabel("Input Feature")
        ax.set_ylabel("Output Variable")
        ax.set_title("Gráfico de Regresión Lineal")
        ax.legend()
        ax.grid(True)  # Añadir rejilla al gráfico

        self.layout.addWidget(canvas)
        canvas.draw()  # Dibuja el gráfico

    def save_model(self):
        # Cambiar el filtro del diálogo para que solo incluya joblib como opción principal
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Modelo",
            "",
            "Joblib (*.joblib);;All Files (*)",
            options=QFileDialog.Option.DontConfirmOverwrite
        )
        
        if file_path:
            # Asegurarse de que la extensión sea .joblib
            if not file_path.endswith('.joblib'):
                file_path += '.joblib'

            try:
                # Extract metrics more safely
                metrics_lines = self.results_label.text().split('\n')
                
                r2_value = 'N/A'
                mse_value = 'N/A'
                
                for line in metrics_lines:
                    if "Coeficiente de determinación (R²)" in line:
                        r2_value = line.split(': ')[1] if ': ' in line else 'N/A'
                    elif "Error Cuadrático Medio (ECM)" in line:
                        mse_value = line.split(': ')[1] if ': ' in line else 'N/A'
                
                model_info = {
                    'description': self.description_text.text(),
                    'metrics': {
                        'R²': r2_value,
                        'MSE': mse_value,
                    },
                    'coefficients': self.model.coef_,
                    'intercept': self.model.intercept_,
                    'input_columns': self.input_columns,
                    'output_column': self.output_column
                }

                joblib.dump(model_info, file_path)  # Guardar el modelo usando joblib
                QMessageBox.information(self, "Done!", f"Model saved successfully in:\n{file_path}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Model couldn't be saved in:\n{str(e)}")

class ModelTrainer(QWidget):
    def __init__(self, data, input_columns, output_column, description=""):
        super().__init__()
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.description = description
        self.model = LinearRegression()

        # Llama a la función de entrenamiento directamente en la inicialización
        self.train_and_show_results()
    
    def train_and_show_results(self):
        try:
            # Preprocesamiento de las columnas de entrada y salida
            X, y = self.preprocess_data(self.input_columns, self.output_column)

            # Dividir en entrenamiento y prueba
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Entrenar el modelo de regresión lineal
            self.model.fit(X_train, y_train)

            # Realizar predicciones y calcular métricas de error en el conjunto de prueba
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            # Mostrar resultados combinados
            self.show_combined_results(mse, r2, X_test, y_test, y_pred)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en la creación del modelo:\n{str(e)}")

    def preprocess_data(self, input_columns, output_column):
        """Preprocess input and output columns, handling categorical variables with OneHotEncoder."""
        X = self.data[input_columns]
        y = self.data[output_column]

        # Categorical columns
        categorical_cols = X.select_dtypes(include=['object', 'category']).columns
        if categorical_cols.any():
            encoder = OneHotEncoder(sparse_output=False, drop='first')
            X_encoded = encoder.fit_transform(X[categorical_cols])

            # Unir las columnas codificadas con las numéricas
            X_numeric = X.drop(columns=categorical_cols).values
            X = np.hstack((X_numeric, X_encoded))
        else:
            # Convertir directamente a valores numpy si no hay variables categóricas
            X = X.values

        return X, y.values

    def show_combined_results(self, mse, r2, X_test, y_test, y_pred):
        coef = self.model.coef_
        intercept = self.model.intercept_

        formula_terms = []
        for i, col in enumerate(self.input_columns):
            formula_terms.append(f"{coef[i]:.4f} * {col}")
        formula = " + ".join(formula_terms)
        formula_text = f"{self.output_column} = {intercept:.4f} + {formula}"

        metrics_text = (f"Métricas del modelo:\n\n"
                        f"Coeficiente de determinación (R²): {r2:.4f}\n"
                        f"Error Cuadrático Medio (ECM): {mse:.4f}\n\n"
                        f"Fórmula del Modelo: {formula_text}")

        num_inputs = self.data[self.input_columns].select_dtypes(include=[np.number])
        warning_text = ""

        if num_inputs.empty:
            warning_text += "Nota: No hay columnas numéricas en los datos de entrada.\n"
        elif len(self.input_columns) > 1 or any(X_test.dtype.kind == 'O' for col in self.input_columns):
            warning_text += "Nota: La gráfica solo se muestra para una columna numérica de entrada."

        plot_data = None
        if len(self.input_columns) == 1 and X_test.shape[1] == 1 and not num_inputs.empty:
            plot_data = (X_test[:, 0], y_test, y_pred)

        # Pass the model to the ResultsWindow
        results_window = ResultsWindow(self.description, metrics_text, plot_data, self.model, self.input_columns, self.output_column, warning_text)
        results_window.exec()