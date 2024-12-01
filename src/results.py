import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import joblib


class ResultsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.init_ui()

    def init_ui(self):
        """Configura la UI del modelo con todos los elementos gráficos básicos."""
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Header
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("background-color: #0b5394;")
        header_widget.setFixedHeight(35)

        # Header buttons
        self.change_description_button = QPushButton("CHANGE DESCRIPTION")
        self.change_description_button.setFixedHeight(28)
        self.change_description_button.setFixedWidth(170)
        self.change_description_button.setStyleSheet(""" 
        QPushButton {
            background-color: transparent; 
            color: white;
            border: 2px solid #F6BE00;
            border-radius: 5px;
            font-weight: bold;
            padding-left: 15px;
            padding-right: 15px;   
        }
        """)
        header_layout.addWidget(self.change_description_button)

        self.description_text = QLabel("No description available")
        self.description_text.setStyleSheet("color: white; font-family: 'Bahnschrift'; font-size: 16px;")
        self.description_text.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.description_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        header_layout.addWidget(self.description_text)

        self.save_button = QPushButton("SAVE MODEL")
        self.save_button.setFixedHeight(28)
        self.save_button.setFixedWidth(170)
        self.save_button.setToolTip("Click to save the trained model to a .joblib file.")
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
        header_layout.addWidget(self.save_button)

        self.layout.addWidget(header_widget)

        # Model metrics
        self.data_group = QGroupBox("Model Metrics:")
        self.data_layout = QVBoxLayout()
        self.results_label = QLabel("")
        self.results_label.setFont(QFont("Bahnschrift", 12))
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.data_layout.addWidget(self.results_label)
        self.data_group.setLayout(self.data_layout)
        self.layout.addWidget(self.data_group)

        # ** Side Layout (Graphic and Prediction) **
        self.side_layout = QHBoxLayout()

        # Left column: Alternate between Graphic and Message
        self.left_column_layout = QStackedWidget()
        self.graph_widget = self.create_graph_widget()
        self.warning_label = QLabel("No data to display.")
        self.warning_label.setStyleSheet("color: red; padding: 10px;")
        self.left_column_layout.addWidget(self.warning_label)  # Warning
        self.left_column_layout.addWidget(self.graph_widget)  # Graph
        self.side_layout.addWidget(self.left_column_layout)

        # Right column: Prediction GroupBox
        self.prediction_group = QGroupBox("Make a Prediction")
        self.prediction_layout = QVBoxLayout()  # Cambiar el layout principal a QVBoxLayout
        self.dynamic_inputs_layout = QFormLayout()  # Layout para los campos dinámicos
        self.input_fields = {}  # Diccionario para almacenar referencias a los campos

        # Añadir el sublayout de campos dinámicos al layout principal
        self.prediction_layout.addLayout(self.dynamic_inputs_layout)

        # Botón de predicción (estático)
        self.predict_button = QPushButton("Make Prediction")
        self.predict_button.setStyleSheet("font-weight: bold; color: #0B5394;")
        self.predict_button.clicked.connect(self.make_prediction)

        # Salida de predicción (estática)
        self.prediction_output = QLabel("")
        self.prediction_output.setStyleSheet("font-weight: bold; color: green;")

        # Añadir el botón y la salida como elementos estáticos
        self.prediction_layout.addWidget(self.predict_button)
        self.prediction_layout.addWidget(self.prediction_output)

        # Configurar el diseño del grupo de predicción
        self.prediction_group.setLayout(self.prediction_layout)
        self.side_layout.addWidget(self.prediction_group)

        # Adjust columns
        self.side_layout.setStretch(0, 3)  # Graphic
        self.side_layout.setStretch(1, 2)  # Prediction

        self.layout.addLayout(self.side_layout)

    def create_graph_widget(self):
        """Create interactive graph widget."""
        container = QWidget()
        container_layout = QVBoxLayout(container)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        container_layout.addWidget(self.toolbar)  # Toolbar on top
        container_layout.addWidget(self.canvas)  # Graph below
        return container

    def update_tab(self, description, r2, mse, formula, plot_data, coef, intercept, input_columns, output_column, warning_text=""):
        """Update values in the UI with provided information."""
        self.input_columns = input_columns
        self.coef = coef
        self.intercept = intercept
        self.description_text.setText(description)
        metrics_text = (f"Coefficient of determination (R²): {r2:.4f}\n"
                        f"Mean Squared Error (MSE): {mse:.4f}\n\n"
                        f"Model Formula: {formula}")
        self.results_label.setText(metrics_text)

        # Update left column
        if plot_data:
            self.plot_regression(plot_data)
            self.left_column_layout.setCurrentWidget(self.graph_widget)
        else:
            self.warning_label.setText(warning_text)
            self.left_column_layout.setCurrentWidget(self.warning_label)

        for i in reversed(range(self.dynamic_inputs_layout.count())):
            widget = self.dynamic_inputs_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()  # Elimina el widget de la memoria

        # Regenerar campos dinámicos
        self.input_fields.clear()  # Reiniciar el diccionario
        for col in self.input_columns:
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Enter value for {col}")
            self.dynamic_inputs_layout.addRow(f"{col}:", input_field)  # Añadir al layout dinámico
            self.input_fields[col] = input_field  # Guardar referencia en el diccionario

        # Limpiar predicción previa
        self.prediction_output.setText("")

    def plot_regression(self, plot_data):
        """Generate or update the regression graph."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        X_test, y_test, y_pred = plot_data

        ax.scatter(X_test, y_test, label="Actual Data", color="blue", alpha=0.7)
        ax.plot(X_test, y_pred, label="Regression Line", color="red", linewidth=2)
        ax.set_title("Regression Plot")
        ax.set_xlabel("Feature")
        ax.set_ylabel("Target")
        ax.legend()
        ax.grid(True)

        self.canvas.draw()

    def save_model(self):
        """Save model to a .joblib file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Model", "", "Joblib (*.joblib);;All Files (*)")
        if file_path:
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
                joblib.dump(model_info, file_path)
                QMessageBox.information(self, "Done!", f"Model saved successfully in:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Model couldn't be saved:\n{str(e)}")

    def make_prediction(self):
        """Generate predictions based on input."""
        try:
            input_values = [float(self.input_fields[col].text()) for col in self.input_columns]
            input_array = np.array(input_values).reshape(1, -1)
            prediction = np.dot(input_array, self.coef) + self.intercept
            self.prediction_output.setText(f"{prediction[0]:.4f}")
        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"Unexpected Error:\n{str(e)}")
