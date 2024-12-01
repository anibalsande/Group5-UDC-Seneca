from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class ModelTrainer(QWidget):
    def __init__(self, data, input_columns, output_column, description=""):
        super().__init__()
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.description = description
        self.model = LinearRegression()
        self.warning_text = ""

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

            # Calculate formula
            self.coef = self.model.coef_
            self.intercept = self.model.intercept_
            formula_terms = [f"{self.coef[i]:.4f} * {col}" for i, col in enumerate(self.input_columns)]
            formula = f"{self.output_column} = {self.intercept:.4f} + {' + '.join(formula_terms)}"

            # Determinar el mensaje de advertencia y los datos de la gráfica
            if len(self.input_columns) > 1:
                self.warning_text = "The graph is only displayed for simple linear regression."

            plot_data = (X_test[:, 0], y_test, y_pred) if len(self.input_columns) == 1 and X_test.shape[1] == 1 else None

            # Pasar métricas, fórmula, y otros datos a ResultsWindow
            if show_window == True:
                self.r2 = r2
                self.mse = mse
                self.formula = formula
                self.plot_data = plot_data

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en la creación del modelo:\n{str(e)}")
