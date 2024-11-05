import numpy as np
from PyQt6.QtWidgets import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ResultsWindow(QDialog):
    def __init__(self, metrics_text, formula_text, plot_data, warning_text=""):
        super().__init__()
        self.setWindowTitle("Resultados del Modelo")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.results_label = QLabel(metrics_text)
        self.warning_label = QLabel(warning_text) if warning_text else QLabel("")

        self.layout.addWidget(self.results_label)
        self.layout.addWidget(self.warning_label)

        # Generar y mostrar el gráfico si hay datos para ello
        if plot_data is not None:
            self.plot_regression_line(plot_data)

        self.setLayout(self.layout)

    def plot_regression_line(self, plot_data):
        X_test, y_test, y_pred = plot_data
        
        # Crear un nuevo widget para el gráfico
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        ax.scatter(X_test, y_test, color="blue", label="Datos reales")
        ax.plot(X_test, y_pred, color="red", label="Recta de ajuste")
        ax.set_xlabel("Input Feature")
        ax.set_ylabel("Output Variable")
        ax.set_title("Gráfico de Regresión Lineal")
        ax.legend()

        self.layout.addWidget(canvas)
        canvas.draw()  # Dibuja el gráfico

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
        """Muestra las métricas, fórmula del modelo, y si aplica, la advertencia de gráfica y el gráfico."""
        coef = self.model.coef_
        intercept = self.model.intercept_

        # Generar fórmula en función de los coeficientes del modelo
        formula_terms = []
        for i, col in enumerate(self.input_columns):
            formula_terms.append(f"{coef[i]:.4f} * {col}")
        formula = " + ".join(formula_terms)
        formula_text = f"{self.output_column} = {intercept:.4f} + {formula}"

        # Mensaje informativo del modelo
        metrics_text = (f"Métricas del modelo:\n\n"
                        f"Coeficiente de determinación (R²): {r2:.4f}\n"
                        f"Error Cuadrático Medio (ECM): {mse:.4f}\n\n"
                        f"Fórmula del Modelo:\n{formula_text}")

        # Check for numeric input columns
        num_inputs = self.data[self.input_columns].select_dtypes(include=[np.number])
        warning_text = ""
        
        if num_inputs.empty:
            warning_text += "Nota: No hay columnas numéricas en los datos de entrada.\n"
        elif len(self.input_columns) > 1 or any(X_test.dtype.kind == 'O' for col in self.input_columns):
            warning_text += "Nota: La gráfica solo se muestra para una columna numérica de entrada."

        # Generar gráfico solo si hay una columna numérica
        plot_data = None
        if len(self.input_columns) == 1 and X_test.shape[1] == 1 and not num_inputs.empty:
            plot_data = (X_test[:, 0], y_test, y_pred)

        # Mostrar la ventana de resultados
        results_window = ResultsWindow(metrics_text, formula_text, plot_data, warning_text)
        results_window.exec()