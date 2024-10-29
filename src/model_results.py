import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QMessageBox
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt

class ModelTrainer:
    def __init__(self, data, input_columns, output_column, description=""):
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.description = description
        self.model = LinearRegression()

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

            # Generar mensaje de resultados, fórmula, y advertencia de gráfica si corresponde
            self.show_combined_results(mse, r2, X_test, y_test, y_pred)

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error en la creación del modelo:\n{str(e)}")

    def preprocess_data(self, input_columns, output_column):
        """Preprocesa las columnas de entrada y salida, manejando variables categóricas con OneHotEncoder."""
        X = self.data[input_columns]
        y = self.data[output_column]

        # Codificación One-Hot para las columnas categóricas
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
        """Muestra las métricas, fórmula del modelo, y si aplica, la advertencia de gráfica y el gráfico."""
        coef = self.model.coef_
        intercept = self.model.intercept_

        # Generar fórmula en función de los coeficientes del modelo
        formula_terms = []
        for i, col in enumerate(self.input_columns):
            formula_terms.append(f"{coef[i]:.4f} * {col}")
        formula = " + ".join(formula_terms)
        formula_text = f"{self.output_column} = {intercept:.4f} + {formula}"

        # Mensaje informativo del modelo y advertencia de gráfica
        message = (f"Métricas del modelo:\n\n"
                   f"Coeficiente de determinación (R²): {r2:.4f}\n"
                   f"Error Cuadrático Medio (ECM): {mse:.4f}\n\n"
                   f"Fórmula del Modelo:\n{formula_text}")

        if len(self.input_columns) > 1 or any(X_test.dtype.kind == 'O' for col in self.input_columns):
            message += "\n\nNota: La gráfica solo se muestra para una columna numérica de entrada."

        # Mostrar mensaje combinado en una ventana
        QMessageBox.information(None, "Resultados del Modelo", message)

        # Generar gráfica si solo hay una columna numérica
        if len(self.input_columns) == 1 and X_test.shape[1] == 1:
            self.plot_regression_line(X_test[:, 0], y_test, y_pred)

    def plot_regression_line(self, X_test, y_test, y_pred):
        """Genera la gráfica de puntos y la línea de regresión si solo hay una variable de entrada numérica."""
        plt.scatter(X_test, y_test, color="blue", label="Datos reales")
        plt.plot(X_test, y_pred, color="red", label="Recta de ajuste")
        plt.xlabel(self.input_columns[0])
        plt.ylabel(self.output_column)
        plt.title("Gráfico de Regresión Lineal")
        plt.legend()
        plt.show()
