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
    """
    A PyQt6-based widget for training a linear regression model and displaying the results.

    Attributes:
        data (DataFrame): The dataset used for training and testing the model.
        input_columns (list): List of column names used as input features.
        output_column (str): The name of the column used as the target variable.
        description (str): An optional description of the model.
        model (LinearRegression): The linear regression model instance.
        warning_text (str): A message indicating any limitations, such as graph display constraints.
    """
    def __init__(self, data, input_columns, output_column, description=""):
        """
        Initializes the ModelTrainer widget.

        Args:
            data (DataFrame): The dataset used for training and testing the model.
            input_columns (list): List of column names used as input features.
            output_column (str): The name of the column used as the target variable.
            description (str, optional): An optional description of the model. Defaults to an empty string.
        """
        super().__init__()
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.description = description
        self.model = LinearRegression()
        self.warning_text = ""

        self.train_and_show_results()
    
    def train_and_show_results(self, show_window = True):
        """
        Trains the linear regression model and optionally displays the results in a separate window.

        Args:
            show_window (bool, optional): Whether to display the results window. Defaults to True.

        Raises:
            QMessageBox: Displays an error message if there is an issue during model training.
        """
        try:
            X = self.data[self.input_columns].values
            y = self.data[self.output_column].values

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
            if show_window == True:
                self.r2 = r2
                self.mse = mse
                self.formula = formula
                self.plot_data = plot_data

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in model creation:\n{str(e)}")
