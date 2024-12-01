import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
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
        self.description_text = QLabel("No description available")
        self.description_text.setStyleSheet("color: white; font-family: 'Bahnschrift'; font-size: 16px;margin-left: 170px;")
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

        # Main content container
        main_content_widget = QWidget()
        main_content_layout = QVBoxLayout()
        main_content_layout.setContentsMargins(10, 0, 10, 10)  # Márgenes uniformes
        main_content_widget.setLayout(main_content_layout)
        self.layout.addWidget(main_content_widget)

        # Model metrics
        self.data_group = QGroupBox("Model Metrics")
        self.data_layout = QVBoxLayout()
        self.data_group.setContentsMargins(0, 0, 0, 0)
        self.data_group.setLayout(self.data_layout)

        self.results_label = QLabel("")
        self.results_label.setFont(QFont("Bahnschrift", 12))
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.data_layout.addWidget(self.results_label)
        main_content_layout.addWidget(self.data_group)

        # Side Layout (Graphic and Prediction)
        self.side_layout = QHBoxLayout()
        self.side_layout.setContentsMargins(0, 0, 0, 0)

        # Left column: Alternate between Graphic and Message
        self.left_column_layout = QStackedWidget()
        self.graph_widget = self.create_graph_widget()
        self.warning_label = QLabel("No data to display.")
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warning_label.setStyleSheet("font-size: 16px;font-family: 'Bahnschrift';font-weight: semi-bold;color: #333;padding: 10px;background-color: #e0e0e0;border-radius: 5px;")

        self.left_column_layout.addWidget(self.warning_label)  # Warning
        self.left_column_layout.addWidget(self.graph_widget)  # Graph
        self.side_layout.addWidget(self.left_column_layout)

        # Right column: Prediction GroupBox
        self.prediction_group = QGroupBox("Prediction")
        self.prediction_layout = QVBoxLayout()  # Diseño principal vertical
        self.dynamic_inputs_layout = QFormLayout()  # Diseño para entradas dinámicas
        self.input_fields = {}  # Diccionario para almacenar campos dinámicos

        # Agregar el diseño de entradas dinámicas al diseño principal
        self.prediction_layout.addLayout(self.dynamic_inputs_layout)

        # Prediction button
        self.predict_button = QPushButton("Make Prediction")
        self.predict_button.setFixedHeight(28)  # Altura fija
        self.predict_button.setFixedWidth(170)  # Ancho fijo
        self.predict_button.setStyleSheet("""
            QPushButton {
                background-color: #0B1E3E; 
                color: white;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #F6BE00;
                color: #0B1E3E;
            }
        """)
        self.predict_button.clicked.connect(self.make_prediction)

        # Etiqueta de salida
        self.output_label = QLabel("Output:")
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar texto
        self.output_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        # Campo de salida
        self.prediction_output = QLabel("")  # Texto vacío por defecto
        self.prediction_output.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar texto de salida
        self.prediction_output.setStyleSheet("font-weight: bold; color: green; font-size: 14px;")

        # Contenedor inferior para los widgets (botón y etiquetas de salida)
        self.bottom_container = QWidget()
        self.bottom_container.setContentsMargins(0, 0, 0, 0)
        self.bottom_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Ajustar solo el alto
        self.bottom_container.setStyleSheet("background-color: #CCE4F6; border-radius: 8px; padding: 10px;")
        self.bottom_layout = QVBoxLayout(self.bottom_container)  # Diseño vertical para el contenedor
        self.bottom_layout.addWidget(self.predict_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.bottom_layout.addWidget(self.output_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.bottom_layout.addWidget(self.prediction_output, alignment=Qt.AlignmentFlag.AlignCenter)

        # Agregar el contenedor inferior al diseño principal
        self.prediction_layout.addStretch()  # Empuja widgets hacia abajo
        self.prediction_layout.addWidget(self.bottom_container)

        # Configurar el diseño en el grupo de predicción
        self.prediction_group.setLayout(self.prediction_layout)

        # Agregar el grupo al diseño lateral
        self.side_layout.addWidget(self.prediction_group)

        # Ajuste de las columnas
        self.side_layout.setStretch(0, 4)  # Graphic
        self.side_layout.setStretch(1, 1)  # Prediction

        main_content_layout.addLayout(self.side_layout)

    def create_graph_widget(self):
        """Create interactive graph widget."""
        container = QWidget()
        container_layout = QVBoxLayout(container)

        self.figure = Figure(tight_layout=True)  
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
            self.plot_regression(plot_data, input_columns, output_column)
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
            input_field.setStyleSheet("font-family: Bahnschrift;")
            self.dynamic_inputs_layout.addRow(f"{col}:", input_field)  # Añadir al layout dinámico
            self.input_fields[col] = input_field  # Guardar referencia en el diccionario

        # Limpiar predicción previa
        self.prediction_output.setText("")

        self.output_label.setText(f"{output_column}:")
        self.prediction_output.setText("")


    def plot_regression(self, plot_data, input, output):
        """Generate or update the regression graph."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        X_test, y_test, y_pred = plot_data

        ax.scatter(X_test, y_test, label="Actual Data", color="blue", alpha=0.7)
        ax.plot(X_test, y_pred, label="Regression Line", color="red", linewidth=2)
        ax.set_xlabel(input[0])
        ax.set_ylabel(output)
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
            # Comprobar si todos los campos de entrada están llenos
            input_values = []
            for col in self.input_columns:
                text = self.input_fields[col].text().strip()
                if not text:  # Si el campo está vacío
                    raise ValueError(f"Input for '{col}' is missing.")
                try:
                    input_values.append(float(text)) 
                except ValueError:
                    raise ValueError(f"Input for '{col}' must be a numeric value.")  

            input_array = np.array(input_values).reshape(1, -1)
            prediction = np.dot(input_array, self.coef) + self.intercept
            self.prediction_output.setText(f"{prediction[0]:.4f}")
        
        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"Unexpected Error:\n{str(e)}") 

