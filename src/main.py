import sys
import pandas as pd
import sqlite3
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import joblib
from sklearn.linear_model import LinearRegression

#Modules
from data_table import DataTable
from model_results import ModelTrainer
from results import ResultsTab
from help import HelpTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LRM APP · GROUP 5")
        self.setGeometry(100, 100, 700, 500)
        self.setFont(QFont("Bahnschrift", 12))
        self.setWindowIcon(QIcon("src/image/icon.png"))

        self.data = None
        self.input_columns = []
        self.output_column = None
        self.model_description = ""

        # Main Layout
        main_layout = QVBoxLayout()

        # Create a Tab Widget
        self.tabs = QTabWidget()
        
        # Add tabs to QTabWidget
        self.data_tab = QWidget()
        self.results_tab = ResultsTab()
        self.help_tab = HelpTab()

        self.tabs.addTab(self.data_tab, QIcon("src/image/database.png"), "DATA")
        self.tabs.addTab(self.results_tab, QIcon("src/image/model.png"), "MODEL")
        self.tabs.addTab(self.help_tab, QIcon("src/image/help.png"), "HELP")
        self.tabs.setTabEnabled(1, False)

        # Setup Tab Contents
        self.setup_data_tab()

        # Set the central widget layout
        container = QWidget()

        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Add tabs to the main layout
        main_layout.addWidget(self.tabs)
        main_layout.setContentsMargins(0, 0, 0, 0)


    def setup_data_tab(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        # Blue header
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("background-color: #0b5394;")
        header_widget.setFixedHeight(35)

        # "OPEN FILE" Button
        self.upload_button = QPushButton("OPEN FILE")
        self.upload_button.setFixedHeight(28)
        self.upload_button.setFixedWidth(170)
        self.upload_button.setStyleSheet(""" 
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
        self.upload_button.clicked.connect(self.select_file)
        header_layout.addWidget(self.upload_button)

        # File name
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: white; font-family: 'Bahnschrift'; font-size: 16px;")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.file_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        header_layout.addWidget(self.file_label)

        self.load_model_button = QPushButton("+ Open Model")
        self.load_model_button.setFixedHeight(28)
        self.load_model_button.setFixedWidth(170)
        self.load_model_button.setStyleSheet(""" 
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
        self.load_model_button.clicked.connect(self.load_model)
        header_layout.addWidget(self.load_model_button)

        # Add header to layout
        main_layout.addWidget(header_widget)
        
        self.table_widget = QStackedWidget()
        self.table_widget.setFixedHeight(420)

        # Table configuration to display data
        self.welcome_label = QLabel("Welcome! No data available.\nPlease import database or an existing model.")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-family: 'Bahnschrift';
                font-weight: semi-bold;
                color: #333;
                padding: 20px;
                background-color: #e0e0e0;
                border: 1px solid #b0b0b0;
            }
        """)

        self.table_view = DataTable()
        self.table_view.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        self.table_widget.addWidget(self.welcome_label)
        self.table_widget.addWidget(self.table_view)

        main_layout.addWidget(self.table_widget)

        # Middle layout
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(10,10,10,10)

        # Column selection side
        self.column_selection_group = QGroupBox("Column Selection")
        self.column_selection_group.setEnabled(False)
        column_selection_layout = QHBoxLayout()
        column_selection_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        # First column (Text and Multi-Selector)
        left_column_layout = QVBoxLayout()
        
        # Features (first column)
        self.input_selector = QListWidget()  # Cambiamos a QListWidget para selección múltiple
        self.input_selector.setSelectionMode(QListWidget.SelectionMode.MultiSelection)  
        self.input_selector.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        left_column_layout.addWidget(QLabel("Features:"))
        left_column_layout.addWidget(self.input_selector)
        self.input_selector.setToolTip("Select the columns that will be used as input features for the model.")


        # Second column (Text, Dropdown)
        right_column_layout = QVBoxLayout()
        target_label = QLabel("Target:")
        target_label.setToolTip("The 'Target' is the dependent variable column we aim to predict.")
        right_column_layout.addWidget(target_label)

        self.output_selector = QListWidget()
        self.output_selector.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)    
        self.output_selector.setToolTip("Select the column that will be used as the target variable.")
        right_column_layout.addWidget(self.output_selector)

        # Confirm button (second column)
        self.confirm_button = QPushButton("Confirm Selection ⮕")
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.confirm_button.setFixedHeight(40) 
        self.confirm_button.setToolTip("Confirms the selected columns as input and output characteristics.")
        self.confirm_button.setStyleSheet(""" 
            QPushButton {
                background-color: #0B1E3E; 
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #F6BE00;
                color: #0B1E3E;
            }
        """)

        # Add the two columns to the main layout
        column_selection_layout.addLayout(left_column_layout)
        column_selection_layout.addLayout(right_column_layout)
        column_selection_layout.addWidget(self.confirm_button)
        column_selection_layout.setAlignment(self.confirm_button, Qt.AlignmentFlag.AlignBottom)

        column_selection_layout.setStretchFactor(left_column_layout, 1)
        column_selection_layout.setStretchFactor(right_column_layout, 1)  

        # Add the main layout to the group
        self.column_selection_group.setLayout(column_selection_layout)

        # Preprocess side
        self.preprocess_group = QGroupBox("Preprocessing Options")
        preprocess_layout = QVBoxLayout()
        self.preprocess_group.setFixedWidth(220)
        preprocess_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.preprocess_group.setEnabled(False)

        # Combobox for Nan
        self.nan_options = QComboBox()
        self.nan_options.addItems([
            "Select Option",
            "Remove rows with NaN",
            "Fill NaN with Mean",
            "Fill NaN with Median",
            "Fill NaN with Constant"
        ])
        self.nan_options.setFixedWidth(200)
        preprocess_layout.addWidget(self.nan_options)
        self.nan_options.setToolTip("Select an option to handle missing values ​​(NaN) in the dataset.")


        # Input constant
        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Enter constant value")
        self.constant_input.setFixedWidth(200)
        self.constant_input.setDisabled(True)
        preprocess_layout.addWidget(self.constant_input)
        self.constant_input.setToolTip("Enter a constant value to replace the NaN values ​​in the columns.")


        # Enable constant input
        self.nan_options.currentIndexChanged.connect(self.toggle_constant_input)

        # Preprocessing button
        self.apply_button = QPushButton("Apply Preprocessing ⮕")
        self.apply_button.clicked.connect(self.apply_preprocessing)
        self.apply_button.setFixedHeight(40)  
        self.apply_button.setFixedWidth(200)  
        self.apply_button.setToolTip("Applies selected preprocessing options for NaN values.")
        self.apply_button.setStyleSheet(""" 
            QPushButton {
                background-color: #0B1E3E; 
                color: white;
                padding: 10px;
                border-radius: 5px;  
                font-weight: bold;  
                font-size: 12px;  
            }
            QPushButton:hover {
                background-color: #F6BE00;
                color: #0B1E3E;
            }
        """)
        preprocess_layout.addWidget(self.apply_button)

        # Configure and add the preprocessing layout to its group
        self.preprocess_group.setLayout(preprocess_layout)

        # Model side
        self.model_group = QGroupBox("Create model")
        model_layout = QVBoxLayout()
        model_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.model_group.setFixedWidth(300)
        self.model_group.setEnabled(False)

        self.description = QTextEdit()
        self.description.setPlaceholderText("Create description")
        self.description.setFixedWidth(280)
        self.output_selector.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)    
        model_layout.addWidget(self.description)

        # Preprocessing button
        self.model_button = QPushButton("Create model ⮕")
        self.model_button.setFixedHeight(40)  
        self.model_button.setFixedWidth(200)  
        self.model_button.setToolTip("Create a regression model based on the data and selected columns.")
        self.model_button.setStyleSheet(""" 
            QPushButton {
                background-color: #0B1E3E; 
                color: white;
                padding: 10px;
                border-radius: 5px;  
                font-weight: bold;  
                font-size: 12px;  
            }
            QPushButton:hover {
                background-color: #F6BE00;
                color: #0B1E3E;
            }
        """)
        model_layout.addWidget(self.model_button)
        self.model_button.clicked.connect(self.create_model)
        
        self.model_group.setLayout(model_layout)

        # Add both groups (Preprocessing and Column Selection) to the horizontal layout
        horizontal_layout.addWidget(self.column_selection_group)  # Column Selection on the left
        horizontal_layout.addWidget(self.preprocess_group)  # Preprocessing Options in the center
        horizontal_layout.addWidget(self.model_group)  # Model

        # Add the horizontal layout to the main layout 
        main_layout.addLayout(horizontal_layout)

        # Main container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connect the changes in the regression type to the input selector update.
        self.input_selector.itemSelectionChanged.connect(self.update_output_selector)
        self.data_tab.setLayout(main_layout)

    def toggle_constant_input(self):
        """ Habilitar o deshabilitar el campo de texto para la constante """
        self.constant_input.setDisabled(self.nan_options.currentIndex() != 4)

    def select_file(self):
        options = QFileDialog.Option.ReadOnly
        self.welcome_label.setText("Importing data...")
        self.table_widget.setCurrentWidget(self.welcome_label)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Dataset", "", "Admitted files (*.csv *.xlsx *.xls *.sqlite *.db)", options=options)
        if file_path:
            try:
                self.welcome_label.setText("Checking NaNs...")
                self.file_label.setText(f"{file_path}")
                self.data = self.data_import(file_path)  
                self.welcome_label.setText("Showing Data...")
                self.check_for_nans()  
                self.input_columns = []  # Attribute to store input columns.
                self.output_column = None
                self.table_view.update_table(self.data)  # Display the data when the file is loaded
                self.table_widget.setCurrentWidget(self.table_view)
                self.populate_columns()
                self.column_selection_group.setEnabled(True)
                self.preprocess_group.setEnabled(False)
                self.model_group.setEnabled(False)

            except Exception as e:
                self.file_label.setText(f"Error: {str(e)}")
                self.file_label.setStyleSheet("QLabel {color: red; padding: 5px;}")
        else:
            self.welcome_label.setText("No file was selected. \nPlease import database or an existing model.")
            

    def data_import(self, file_path):
        """ Import the data from the file """
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        elif file_path.endswith('.sqlite') or file_path.endswith('.db'):
            conn = sqlite3.connect(file_path)
            query = "SELECT * FROM sqlite_master WHERE type='table';"
            tables = pd.read_sql(query, conn)
            if not tables.empty:
                table_name = tables.iloc[0]['name']
                return pd.read_sql(f"SELECT * FROM {table_name}", conn)
            else:
                raise ValueError("No tables found in the SQLite database.")
        else:
            raise ValueError("Unsupported file format.")

    def check_for_nans(self):
        """Check for NaN or empty values in the DataFrame and display a message to the user."""
        if self.data is not None:
            # Summary of NaN values per column
            nan_summary = self.data.isnull().sum()

            # Filter columns that contain NaN values
            nan_columns = nan_summary[nan_summary > 0]

            if not nan_columns.empty:
                # Build the list with the column information, using <br> for line breaks
                columns_info = '<br>'.join(f"{col}: {count}" for col, count in nan_columns.items())
                
                # Display the message with HTML format to include the horizontal line
                QMessageBox.warning(
                    self,
                    "Missing Data (NaN) Detected",
                    f"The following columns contain missing values:<br>{columns_info}"
                )

            else:
                # Inform that no NaN values were found
                QMessageBox.information(
                    self,
                    "Data is Complete",
                    "No missing values (NaN) were found in the dataset."
                )
                self.model_group.setEnabled(True)

    
    def apply_preprocessing(self):
        if self.data is None:
            QMessageBox.warning(self, "Error", "No dataset loaded.")
            return
        option = self.nan_options.currentText()

        # Apply the selected preprocessing
        try:
            if option == "Remove rows with NaN":
                self.data = self.data.dropna()
            elif option == "Fill NaN with Mean":
                self.data = self.fill_with_statistic(self.data, "mean")
            elif option == "Fill NaN with Median":
                self.data = self.fill_with_statistic(self.data, "median")
            elif option == "Fill NaN with Constant":
                constant_value = self.constant_input.text()
                if not constant_value:
                    raise ValueError("Please enter a constant value.")
                self.data.fillna(value=float(constant_value), inplace=True)
            else:
                raise ValueError("Please select a valid option.")

            self.table_view.update_table(self.data, self.input_columns, self.output_column)  # Display the preprocessed data
            self.model_group.setEnabled(True)
            QMessageBox.information(self, "Success", "Data preprocessing completed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during preprocessing:\n{str(e)}")

        
    def fill_with_statistic(self, data, stat_type):
        if stat_type not in ["mean", "median"]:
            raise ValueError("Invalid statistic type.")

        for column in data.columns:
            if data[column].dtype in [int, float]:  # Only process numeric columns
                if stat_type == "mean":
                    data[column] = data[column].fillna(data[column].mean())
                elif stat_type == "median":
                    data[column] = data[column].fillna(data[column].median())
        return data

    def confirm_selection(self):
        """ Confirm column selection """
        if self.data is None:
            QMessageBox.warning(self, "Warning", "No data loaded!")
            return

        selected_inputs = self.input_selector.selectedItems()
        selected_output = self.output_selector.selectedItems()

        if not selected_inputs or not selected_output:
            QMessageBox.warning(self, "Warning", "Please select input features and output target!")
            return

        self.input_columns = [item.text() for item in selected_inputs]
        self.output_column = selected_output[0].text()

        QMessageBox.information(self, "Selection Confirmed",
                                f"Input Columns: {', '.join(self.input_columns)}\nOutput Column: {self.output_column}")
        self.table_view.update_table(self.data, self.input_columns, self.output_column)  # Display the table after confirming the selection
        self.preprocess_group.setEnabled(True)

    def populate_columns(self):
        """ Fill the column selectors with the names of numeric columns """
        if self.data is not None:
            numeric_columns = self.data.select_dtypes(include=["number"]).columns.tolist()
            self.input_selector.clear()
            self.input_selector.addItems(numeric_columns)
            self.output_selector.clear()
            self.output_selector.addItems(numeric_columns)

    def update_output_selector(self):
        selected_inputs = [item.text() for item in self.input_selector.selectedItems()]
        numeric_columns = self.data.select_dtypes(include=["number"]).columns
        remaining_columns = [col for col in numeric_columns if col not in selected_inputs]
        
        self.output_selector.clear()
        self.output_selector.addItems(remaining_columns)

    def create_model(self):
        description_text = self.description.toPlainText().strip()
        # Check if the description is empty.
        if not description_text:
            response = QMessageBox.question(
                self, "Empty Description",
                "The model description is empty. Do you want to proceed without a description?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            # If the user selects "No", stop the process so they can modify the description.
            if response == QMessageBox.StandardButton.No:
                return  # Salir de la función sin continuar

        # Assign the final description after the user's decision.
        self.model_description = description_text or "No description provided"

        # Create an instance of ModelTrainer and call its method to train and display the results.
        trainer = ModelTrainer(self.data, self.input_columns, self.output_column, self.model_description)
        self.results_tab.update_tab(
                        description=self.model_description,
                        r2=trainer.r2,
                        mse=trainer.mse,
                        formula=trainer.formula,
                        plot_data=trainer.plot_data,
                        coef=trainer.coef,
                        intercept=trainer.intercept,
                        input_columns=trainer.input_columns,
                        output_column=trainer.output_column,
                        warning_text=trainer.warning_text)
        QMessageBox.information(self, "Successful Load", "The model has been successfully generated.")
        self.tabs.setCurrentIndex(1)
        self.tabs.setTabEnabled(1, True)


    def load_model(self, show_window = True):
        # Dialog to select the file.
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Cargar Modelo",
            "",
            "Joblib (*.joblib);;Pickle (*.pkl);;All Files (*)"
        )

        if file_path:
            try:
                # Load the saved model.
                model_info = joblib.load(file_path)

                # Extract information from the model.
                description = model_info.get('description', 'Without description')
                coefficients = model_info.get('coefficients', [])
                intercept = model_info.get('intercept', 0)
                metrics = model_info.get('metrics', {})
                r2 = metrics.get('R²', 'N/A')
                mse = metrics.get('MSE', 'N/A')
                formula = model_info.get('formula', 'N/A')
                input_columns = model_info.get('input_columns', [])
                output_column = model_info.get('output_column', '')

                # Create the linear regression model using the coefficients and intercept from the loaded model.
                model = LinearRegression()
                model.coef_ = coefficients
                model.intercept_ = intercept

                # Prepare the data for the graph (this can be modified according to your needs).
                plot_data = None 

                # Pass the data to the ResultsWindow with the correct parameters.
                self.results_tab.update_tab(
                        description=description,
                        r2=r2,
                        mse=mse,
                        formula=formula,
                        plot_data=plot_data,
                        coef=coefficients,
                        intercept=intercept,
                        input_columns=input_columns,
                        output_column=output_column,
                        warning_text = "The graph is not displayed for uploaded models."
                    )
                QMessageBox.information(self, "Successful Load", "The model has been uploaded successfully.")
                self.tabs.setTabEnabled(1, True)
                self.tabs.setCurrentIndex(1)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"The model could not be loaded:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # Apply the CSS style correctly.
    app.setStyleSheet("""
        QMainWindow {
            background-color: #0b5394;
        }

        QTabWidget::tab-bar {
            alignment: center;
        }

        QTabBar::tab:selected {
            background: #073763; 
        }

        QTabBar::tab {
            background: #0A4B85;
            font-family: 'Bahnschrift';
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            font-size: 12px;
            font-weight: bold;
            color: white;
            height: 20px;
            width: 150px;
            padding: 5px;
            margin: 0px;
            margin-left: 10px;
            margin-right: 10px;
        }

        QTabBar::tab:hover {
            background: #0B1E3E;
        }
        
        QTabWidget::pane {
            border: none;
            background: white; 
        }

        QTabBar::tab:disabled {
            background: #d3d3d3;  
            color: #a9a9a9; 
        }
                         
        QMessageBox {
        color: #0A4B85;  
        }
    """)

    window.show()
    sys.exit(app.exec())