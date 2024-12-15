from PyQt6.QtWidgets import QFileDialog

from views.datatab import MainView
"""from models.datahandler import DataHandler
from models.createmodel import CreateModel
from models.prediction import Prediction"""

class MainController:
    def __init__(self):
        """self.data_handler = DataHandler()
        self.create_model = CreateModel()
        self.prediction = Prediction()"""
        self.main_window = MainView()

        self.main_window.upload_button.clicked.connect(self.action_openfile)
        """self.main_window.load_model_button.clicked.connect(self.action_openmodel)
        self.main_window.confirm_button.clicked.connect(self.action_columnselection)
        self.main_window.apply_button.clicked.connect(self.action_handlenans)
        self.main_window.create_model_button.clicked.connect(self.action_createmodel)"""

        self.main_window.show()

    def action_openfile(self):
        file_path = self.select_file(title="Select Dataset", file_filter="Admitted files (*.csv *.xlsx *.xls *.sqlite *.db)")
        if file_path:
            self.main_window.file_label.setText(f"File selected: {file_path}")
            self.main_window.file_label.setStyleSheet("QLabel {color: green;}")
            print(f"File selected: {file_path}")
        else:
            self.main_window.file_label.setText("No file selected")
            self.main_window.file_label.setStyleSheet("QLabel {color: red;}")

    def select_file(self, title="Select Dataset", file_filter="Admitted files (*.csv *.xlsx *.xls *.sqlite *.db)"):
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self.main_window, title, "", file_filter, options=options)
        return file_path
