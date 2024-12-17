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
    """
    A PyQt6-based widget for displaying the results of a regression model, including metrics, graphs, and predictions.

    Attributes:
        description_text (QLabel): Label displaying the model's description.
        save_button (QPushButton): Button to save the model to a file.
        results_label (QLabel): Label to display model metrics like R² and MSE.
        graph_widget (QWidget): Widget containing the regression graph.
        warning_label (QLabel): Label to show warnings or messages when no data is available for graphing.
        prediction_group (QGroupBox): GroupBox containing prediction-related inputs and outputs.
        input_fields (dict): Dictionary mapping input column names to their respective QLineEdit widgets.
        prediction_output (QLabel): Label to display the prediction output.
        figure (Figure): Matplotlib figure for the regression graph.
        canvas (FigureCanvas): Canvas to render the Matplotlib figure.
        toolbar (NavigationToolbar): Toolbar for interacting with the graph.
    """
    def __init__(self):
        """
        Initializes the ResultsTab widget and sets up the user interface.
        """
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.init_ui()

    def init_ui(self):
        """
        Set up the model UI with all the basic graphical elements
        """
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
        header_layout.addWidget(self.save_button)

        self.layout.addWidget(header_widget)

        # Main content container
        main_content_widget = QWidget()
        main_content_layout = QVBoxLayout()
        main_content_layout.setContentsMargins(10, 0, 10, 10)  
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

        self.left_column_layout.addWidget(self.warning_label)  
        self.left_column_layout.addWidget(self.graph_widget)  
        self.side_layout.addWidget(self.left_column_layout)

        # Right column: Prediction GroupBox
        self.prediction_group = QGroupBox("Prediction")
        self.prediction_layout = QVBoxLayout()  # Vertical main layout
        self.dynamic_inputs_layout = QFormLayout()  # Layout for dynamic inputs
        self.input_fields = {}  # Dictionary to store dynamic fields

        # Add the dynamic input layout to the main layout
        self.prediction_layout.addLayout(self.dynamic_inputs_layout)

        # Prediction button
        self.predict_button = QPushButton("Make Prediction")
        self.predict_button.setFixedHeight(28)  
        self.predict_button.setFixedWidth(170)  
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

        # Output label
        self.output_label = QLabel("Output:")
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        self.output_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        # Output field
        self.prediction_output = QLabel("")  
        self.prediction_output.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        self.prediction_output.setStyleSheet("font-weight: bold; color: green; font-size: 14px;")

        # Bottom container for widgets (button and output labels)
        self.bottom_container = QWidget()
        self.bottom_container.setContentsMargins(0, 0, 0, 0)
        self.bottom_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  
        self.bottom_container.setStyleSheet("background-color: #CCE4F6; border-radius: 8px; padding: 10px;")
        self.bottom_layout = QVBoxLayout(self.bottom_container)  
        self.bottom_layout.addWidget(self.predict_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.bottom_layout.addWidget(self.output_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.bottom_layout.addWidget(self.prediction_output, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add the bottom container to the main layout
        self.prediction_layout.addStretch()  # Push widgets down
        self.prediction_layout.addWidget(self.bottom_container)

        # Set up the layout in the prediction group
        self.prediction_group.setLayout(self.prediction_layout)

        # Add the group to the side layout
        self.side_layout.addWidget(self.prediction_group)

        # Adjust the columns
        self.side_layout.setStretch(0, 4)  # Graphic
        self.side_layout.setStretch(1, 1)  # Prediction

        main_content_layout.addLayout(self.side_layout)

    def create_graph_widget(self):
        """
        Create interactive regression graph widget.

        Returns:
            QWidget: A container widget with a Matplotlib canvas and toolbar.
        """
        container = QWidget()
        container_layout = QVBoxLayout(container)

        self.figure = Figure(tight_layout=True)  
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        container_layout.addWidget(self.toolbar)  
        container_layout.addWidget(self.canvas)  
        return container
    

    def update_tab(self, description, plot_data, r2, mse, formula, coef, intercept, input_columns, output_column, warning_text=""):
        """
        Update values in the UI with provided information.
        Args:
            description (str): Model description.
            r2 (float): Coefficient of determination (R²).
            mse (float): Mean squared error.
            formula (str): Regression formula.
            plot_data (tuple): Data for plotting (X_test, y_test, y_pred).
            coef (list): Model coefficients.
            intercept (float): Model intercept.
            input_columns (list): List of input feature names.
            output_column (str): Name of the target variable.
            warning_text (str, optional): Warning message for graphing limitations. Defaults to "".
        """   
        self.r2 = r2
        self.mse = mse
        self.formula = formula
        self.coef = coef
        self.intercept = intercept
        self.input_columns = input_columns
        self.output_column = output_column
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
                widget.deleteLater()  # Remove the widget from memory

        # Regenerate dynamic fields
        self.input_fields.clear()  # Reset the dictionary
        for col in self.input_columns:
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Enter value for {col}")
            input_field.setStyleSheet("font-family: Bahnschrift;")
            self.dynamic_inputs_layout.addRow(f"{col}:", input_field)  # Add to the dynamic layout
            self.input_fields[col] = input_field  # Save reference in the dictionary

        # Clear previous prediction
        self.prediction_output.setText("")

        self.output_label.setText(f"{output_column}:")
        self.prediction_output.setText("")


    def plot_regression(self, plot_data, input, output):
        """
        Generate or update the regression graph.

        Args:
            plot_data (tuple): Data for plotting (X_test, y_test, y_pred).
            input (list): List of input feature names.
            output (str): Name of the target variable.
        """
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

    def make_prediction(self):
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
            self.prediction_output.setText(f"{prediction[0]:.4f}")
        
        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"Unexpected Error:\n{str(e)}") 

