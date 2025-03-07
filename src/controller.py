from PyQt6.QtWidgets import *

from views.datatab import MainView
from models.datahandler import DataHandler
from models.modelhandler import ModelHandler

class MainController:
    """
    The MainController class serves as the intermediary between the models and the views MVC.
    It handles user inputs, interacts with the models to retrieve or modify data, and then passes that data to the views.
    """
    def __init__(self):
        self.main_window = MainView()
        self.data_handler = None
        self.model_handler = None

        # Connect UI buttons to corresponding controller methods
        self.main_window.upload_button.clicked.connect(self.action_openfile)
        self.main_window.load_model_button.clicked.connect(self.action_openmodel)
        self.main_window.confirm_button.clicked.connect(self.action_columnselection)
        self.main_window.apply_button.clicked.connect(self.action_handlenans)
        self.main_window.model_button.clicked.connect(self.action_createmodel)
        self.main_window.results_tab.save_button.clicked.connect(self.action_savemodel)
        self.main_window.results_tab.predict_button.clicked.connect(self.action_prediction)

        self.main_window.show()

    def action_openfile(self):
        """
        Handles file selection, data import, and checks for missing values (NaN) in the dataset.
        Updates the UI to show data or error messages as needed.      
        """
        self.main_window.welcome_label.setText("Importing data...")
        file_path = self.select_file(title="Select Dataset", file_filter="Admitted files (*.csv *.xlsx *.xls *.sqlite *.db)")
        self.main_window.table_widget.setCurrentWidget(self.main_window.welcome_label)
        if file_path:
            try:
                # Load data using DataHandler
                self.data_handler = DataHandler(file_path)

                # Update file label in the UI
                self.main_window.file_label.setText(f"File selected: {file_path}")
                self.main_window.file_label.setStyleSheet("QLabel {color: white;}")

                # Check for NaN values
                self.main_window.welcome_label.setText("Checking NaNs...")
                nan_columns = self.data_handler.check_for_nans()
                self.main_window.welcome_label.setText("Showing Data...")
                self.main_window.hide_nans_widget(nan_columns)

                if nan_columns is not None:
                    columns_info = '<br>'.join(f"{col}: {count}" for col, count in nan_columns.items())
                    QMessageBox.warning(
                        self.main_window,
                        "Missing Data (NaN) Detected",
                        f"The following columns contain missing values:<br>{columns_info}"
                    )
                else:
                    QMessageBox.information(
                        self.main_window,
                        "Data is Complete",
                        "No missing values (NaN) were found in the dataset."
                    )

                # Display data in the table view
                self.main_window.table_view.update_table(self.data_handler.data)
                self.main_window.table_widget.setCurrentWidget(self.main_window.table_view)
                self.populate_columns()
                # Enable relevant UI elements
                self.main_window.column_selection_group.setEnabled(True)

            except Exception as e:
                self.main_window.file_label.setText(f"Error: {str(e)}")
                self.main_window.file_label.setStyleSheet("QLabel {color: red;}")
        else:
            self.main_window.column_selection_group.setEnabled(True)
            self.main_window.file_label.setText("No file selected")
            self.main_window.file_label.setStyleSheet("QLabel {color: red;}")
            self.main_window.welcome_label.setText("The file could not be loaded.\nPlease import database or an existing model.")


    def select_file(self, title="Select Dataset", file_filter="Admitted files (*.csv *.xlsx *.xls *.sqlite *.db)"):
        """
        Asks the user to select a file using a file dialog.
        
        Args:
            title (str): Title of the file dialog.
            file_filter (str): Filter for acceptable file types.
        
        Returns:
            str: The selected file path.
        """
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self.main_window, title, "", file_filter, options=options)
        return file_path
    
    def populate_columns(self):
        """
        Populates the input and output column selectors with available numeric columns from the data.
        """
        numeric_columns = self.data_handler.get_numeric_columns()
        self.main_window.populate_selectors(numeric_columns)

    def action_columnselection(self):
        """
        Handles the selection of input and output columns by the user.
        Ensures both inputs and outputs are selected, and updates the data handler accordingly.
        """

        selected_inputs = self.main_window.input_selector.selectedItems()
        selected_output = self.main_window.output_selector.selectedItems()

        if not selected_inputs or not selected_output:
            QMessageBox.warning(self.main_window, "Warning", "Please select input features and output target!")
            return

        input_columns = [item.text() for item in selected_inputs]
        output_column = selected_output[0].text()
        self.data_handler.input_columns = input_columns
        self.data_handler.output_column = output_column

        QMessageBox.information(self.main_window, "Selection Confirmed",
                                f"Input Columns: {', '.join(input_columns)}\nOutput Column: {output_column}")
        self.main_window.table_view.update_table(self.data_handler.data, input_columns, output_column)
        if self.data_handler.nans:
            self.main_window.preprocess_group.setEnabled(True)
        else:
            self.main_window.model_group.setEnabled(True)

    def action_handlenans(self):
        """
        Applies preprocessing to handle missing values (NaN) in the dataset based on the user's selection.
        """
        option = self.main_window.nan_options.currentText()
        constant_value = self.main_window.constant_input.text() if option == "Fill NaN with Constant" else None
        try:
            self.data = self.data_handler.apply_preprocessing(option, constant_value)
            self.main_window.table_view.update_table(self.data, self.data_handler.input_columns, self.data_handler.output_column)
            self.main_window.model_group.setEnabled(True)
            QMessageBox.information(self.main_window, "Success", "Data preprocessing completed successfully.")
        except ValueError as ve:
            QMessageBox.warning(self.main_window, "Preprocessing Error", f"Input Error: {str(ve)}")
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"An error occurred during preprocessing:\n{str(e)}")

    def action_openmodel(self):
        """
        Handles the selection and loading of a pre-trained model file.
        Displays a success message or an error if the model cannot be loaded.
        """
        try:
            file_path = self.select_file(title="Select Model", file_filter="Admitted files (*.joblib *.pkl)")        
            if file_path:
                self.model_handler = ModelHandler()
                self.model_handler.load_model(file_path)
                QMessageBox.information(self.main_window, "Success", "Model loaded successfully.")
                self.showmodel("The graph is not displayed for uploaded models.")
            else:
                raise ValueError("No file selected")
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Error loading model:\n{str(e)}")
        

    def action_createmodel(self):
        """
        Trains a new model using the selected input and output columns.
        Displays a success or error message based on the outcome.
        """
        description = self.main_window.description.toPlainText().strip()
        if not description:
            response = QMessageBox.question(
                self.main_window, "Empty Description",
                "The model description is empty. Do you want to proceed without a description?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            # If the user selects "No", stop the process so they can modify the description.
            if response == QMessageBox.StandardButton.No:
                return
        try:
            self.model_handler = ModelHandler()
            self.model_handler.train_model(self.data_handler.data, self.data_handler.input_columns, self.data_handler.output_column, description)
            QMessageBox.information(self.main_window, "Successful Load", "The model has been succesfully generated.")
            if len(self.model_handler.input_columns) > 1:
                self.showmodel("The graph is only displayed for simple linear regression.")
            else:
                self.showmodel()
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"The model could not be loaded:\n{str(e)}")

    def showmodel(self, warning_text = ""):
        """
        Updates the UI to display model results, including metrics and any warnings.
    
        Args:
            warning_text (str): Optional warning message to be displayed.
        """
        description = self.model_handler.description
        if description == "":  # If description is None, assign a value
            description = "No description provided"

        self.main_window.results_tab.update_tab(
            self.model_handler.plot_data,
            self.model_handler.metrics['R²'],
            self.model_handler.metrics['MSE'],
            self.model_handler.formula,
            self.model_handler.input_columns,
            self.model_handler.output_column,
            description, warning_text)
        self.main_window.tabs.setTabEnabled(1, True)
        self.main_window.tabs.setCurrentIndex(1)

    def action_prediction(self):
        """
        Makes predictions using the loaded model and displays the results.
        Handles exceptions related to input errors and unexpected errors.
        """
        try:
            prediction = self.model_handler.make_prediction(self.main_window.results_tab.input_fields)
            self.main_window.results_tab.prediction_output.setText(f"{prediction[0]:.4f}")
        except ValueError as ve:
            QMessageBox.warning(self.main_window, "Input Error", str(ve))  # Display a clear message to the user
        except Exception as e:
            QMessageBox.critical(self.main_window, "Prediction Error", f"Unexpected Error:\n{str(e)}")

    def action_savemodel(self):
        """
        Asks the user to save the model to a specified location.
        Displays a success or error message based on the result.
        """
        file_path, _ = QFileDialog.getSaveFileName(self.main_window, "Save Model", "", "Admitted files (*.joblib *.pkl)")
        if file_path:
            success, message = self.model_handler.save_model(file_path)
            if success:
                QMessageBox.information(self.main_window, "Done!", message)
            else:
                QMessageBox.critical(self.main_window, "Error", message)