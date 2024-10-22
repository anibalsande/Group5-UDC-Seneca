import sys
import pandas as pd
import sqlite3
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
    QVBoxLayout, QWidget, QFileDialog, QTableView, QMessageBox, QAbstractScrollArea, QHeaderView, 
    QComboBox, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QFont

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Upload and Preprocess Dataset")
        self.setGeometry(100, 100, 800, 600)
        font = QFont("Bahnschrift", 12)
        self.setFont(font)

        self.layout = QVBoxLayout()

        self.file_title = QLabel("LINEAR REGRESSION")
        self.file_title.setFont(QFont("Bahnschrift", 20, QFont.Weight.Bold)) 
        self.file_title.setStyleSheet("QLabel {color: #0B1E3E; padding: 5px;}")
        self.file_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.file_title)

        self.button = QPushButton("UPLOAD DATASET")
        self.button.clicked.connect(self.select_file)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #F6BE00; color: #0B1E3E;
                padding: 10px;
                border-radius: 3px;
                font-weight: bold;
                }
            QPushButton:hover {
                background-color: #0B1E3E;
                color: white;
                font-weight: bold;
                }
            """)

        self.layout.addWidget(self.button)

        self.file_label = QLabel("File path:")
        self.file_label.setFont(font)
        self.file_label.setStyleSheet("QLabel {color: #0B1E3E; padding: 5px;}")
        self.layout.addWidget(self.file_label)

        self.table_view = QTableView()
        self.table_view.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table_view.setStyleSheet("""
            QTableView {
                background-color: #f0f0f0;
                gridline-color: black;
                color: black
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #dcdcdc;
                padding: 5px;
                font-weight: bold;
                border: 1px solid #b0b0b0;
            }
        """)

        self.layout.addWidget(self.table_view)

        # Dropdown for preprocessing options
        self.process_option_label = QLabel("Select Missing Value Strategy:")
        self.process_option_label.setFont(font)
        self.process_option_label.setStyleSheet("QLabel {color: #0B1E3E; padding: 5px;}")
        self.layout.addWidget(self.process_option_label)

        self.process_option = QComboBox()
        self.process_option.addItems(["Drop rows with NaN", "Fill with mean", "Fill with median", "Fill with constant"])
        self.layout.addWidget(self.process_option)

        # Input for constant value (only visible when selected)
        self.constant_input_label = QLabel("Enter Constant Value:")
        self.constant_input_label.setFont(font)
        self.constant_input_label.setStyleSheet("QLabel {color: #0B1E3E; padding: 5px;}")
        self.constant_input_label.hide()  # Initially hidden
        self.layout.addWidget(self.constant_input_label)

        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Enter value...")
        self.constant_input.hide()  # Initially hidden
        self.layout.addWidget(self.constant_input)

        self.process_option.currentTextChanged.connect(self.toggle_constant_input)

        # Button to apply preprocessing
        self.preprocess_button = QPushButton("APPLY PREPROCESSING")
        self.preprocess_button.clicked.connect(self.apply_preprocessing)
        self.preprocess_button.setStyleSheet("""
            QPushButton {
                background-color: #00A2E8; color: white;
                padding: 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0B1E3E;
                color: white;
                font-weight: bold;
            }
        """)
        self.layout.addWidget(self.preprocess_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.data = None  # To store the loaded data

    def toggle_constant_input(self, option):
        if option == "Fill with constant":
            self.constant_input_label.show()
            self.constant_input.show()
        else:
            self.constant_input_label.hide()
            self.constant_input.hide()

    def select_file(self):
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
        self, "Select Dataset", "", "Admitted files (*.csv *.xlsx *.xls *.sqlite *.db)", options=options)
        
        if file_path:
            try:
                self.file_label.setText(f"File path: {file_path}")
                self.data = self.data_import(file_path)

                self.display_data(self.data)
                self.detect_missing_values(self.data)
            except Exception as e:
                self.show_error_message(str(e))

    def data_import(self, file):
        if file.endswith(".csv"):
            data = pd.read_csv(file)
            if data.empty:
                raise ValueError("CSV file is empty.")
            return data

        elif file.endswith((".xlsx", ".xls")):
            data = pd.read_excel(file)
            if data.empty:
                raise ValueError("Excel file is empty.")
            return data

        elif file.endswith((".sqlite", ".db")):
            connection = sqlite3.connect(file)
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            cursor = connection.cursor()
            cursor.execute(query)
            tablas = cursor.fetchall()
            if len(tablas) == 0:
                raise ValueError("No tables found in the database.")
            tabla = tablas[0][0]
            data = pd.read_sql_query(f"SELECT * FROM {tabla}", connection)
            connection.close()
            return data

        else:
            raise ValueError("File format not supported.")

    def display_data(self, data):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(data.columns)

        for row in data.itertuples(index=False):
            items = [QStandardItem(str(item)) for item in row]
            model.appendRow(items)

        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def detect_missing_values(self, data):
        missing_data = data.isnull().sum()
        columns_with_nan = missing_data[missing_data > 0]
        
        if not columns_with_nan.empty:
            message = "Missing values detected in the following columns:\n"
            for column, count in columns_with_nan.items():
                message += f"{column}: {count} missing values\n"
            self.show_message_box("Missing Data Detected", message)
        else:
            self.show_message_box("No Missing Data", "No missing values found in the dataset.")

    def apply_preprocessing(self):
        if self.data is None:
            self.show_error_message("No data loaded.")
            return

        option = self.process_option.currentText()

        try:
            if option == "Drop rows with NaN":
                self.data.dropna(inplace=True)
            elif option == "Fill with mean":
                numeric_columns = self.data.select_dtypes(include=["number"]).columns
                self.data[numeric_columns] = self.data[numeric_columns].fillna(self.data[numeric_columns].mean())
            elif option == "Fill with median":
                numeric_columns = self.data.select_dtypes(include=["number"]).columns
                self.data[numeric_columns] = self.data[numeric_columns].fillna(self.data[numeric_columns].median())
            elif option == "Fill with constant":
                constant_value = self.constant_input.text()
                if constant_value == "":
                    raise ValueError("Constant value is required.")
                self.data.fillna(float(constant_value), inplace=True)

            self.display_data(self.data)
            self.show_message_box("Success", "Preprocessing applied successfully!")
        except Exception as e:
            self.show_error_message(f"Error during preprocessing: {str(e)}")

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec())  
        
