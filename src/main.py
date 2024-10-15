import sys
import pandas as pd
import sqlite3
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel,
    QVBoxLayout, QWidget, QFileDialog, QTableView, QMessageBox, QAbstractScrollArea, QProgressBar, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QFont

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Upload Dataset")
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
                gridline-color: #d0d0d0;
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

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)


    def select_file(self):
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
        self, "Select Dataset", "", "Admitted files (*.csv *.xlsx *.xls *.sqlite *.db)", options=options)
            
        if file_path:
            try:
                self.file_label.setText(f"File path: {file_path}")
                data = self.data_import(file_path)

                self.display_data(data)
            except Exception as e:
                self.show_error_message(str(e))

    def data_import(self, file):
        if file.endswith(".csv"):
            data = pd.read_csv(file)
            if data.empty:
                raise ValueError("El archivo CSV está vacío.")
            return data

        elif file.endswith((".xlsx", ".xls")):
            data = pd.read_excel(file)
            if data.empty:
                raise ValueError("El archivo Excel está vacío.")
            return data


        elif file.endswith((".sqlite", ".db")):
            connection = sqlite3.connect(file)
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            cursor = connection.cursor()
            cursor.execute(query)
            tablas = cursor.fetchall()
            if len(tablas) == 0:
                raise ValueError("No se encontraron tablas en la base de datos.")
            tabla = tablas[0][0]
            data = pd.read_sql_query(f"SELECT * FROM {tabla}", connection)
            connection.close()
            return data

        else:
                raise ValueError("Formato de file no soportado.")

    def display_data(self, data):
        model = QStandardItemModel()
        
        model.setHorizontalHeaderLabels(data.columns)

        for row in data.itertuples(index=False):
            items = [QStandardItem(str(item)) for item in row]
            model.appendRow(items)

        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec())