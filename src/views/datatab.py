from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

#Modules
from data_table import DataTable
from model_results import ModelTrainer
from results import ResultsTab
from help import HelpTab

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LRM APP · GROUP 5")
        self.setGeometry(100, 100, 700, 500)
        self.setFont(QFont("Bahnschrift", 12))
        self.setWindowIcon(QIcon("src/image/icon.png"))

        self.setup_ui()

    def setup_ui(self):
        # Main Layout
        main_layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()
        self.data_tab = QWidget()
        self.results_tab = ResultsTab()
        self.help_tab = HelpTab()

        self.tabs.addTab(self.data_tab, QIcon("src/image/database.png"), "DATA")
        self.tabs.addTab(self.results_tab, QIcon("src/image/model.png"), "MODEL")
        self.tabs.addTab(self.help_tab, QIcon("src/image/help.png"), "HELP")
        self.tabs.setTabEnabled(1, False)

        # Data Tab UI
        self.setup_data_tab()

        # Central Widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Add Tabs to Layout
        main_layout.addWidget(self.tabs)
        main_layout.setContentsMargins(0, 0, 0, 0)

    def setup_data_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Blue Header
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        header_widget.setFixedHeight(35)
        header_widget.setStyleSheet("background-color: #0b5394;")

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.upload_button = QPushButton("OPEN FILE")
        self.upload_button.setFixedSize(170, 28)

        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: white; font-family: 'Bahnschrift'; font-size: 16px;")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.file_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.load_model_button = QPushButton("+ Open Model")
        self.load_model_button.setFixedSize(170, 28)

        header_layout.addWidget(self.upload_button)
        header_layout.addWidget(self.file_label)
        header_layout.addWidget(self.load_model_button)
                                     
        layout.addWidget(header_widget)
        
        # Data Table
        self.table_widget = QStackedWidget()
        self.table_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

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

        layout.addWidget(self.table_widget)

        # Column Selection & Preprocessing
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(10,10,10,10)

        self.column_selection_group = self.create_column_selection_group()
        self.preprocess_group = self.create_preprocess_group()
        self.model_group = self.create_model_group()

        self.column_selection_group.setEnabled(False)
        self.preprocess_group.setEnabled(False)
        self.model_group.setEnabled(False)
        
        horizontal_layout.addWidget(self.column_selection_group)
        horizontal_layout.addWidget(self.preprocess_group)
        horizontal_layout.addWidget(self.model_group)

        layout.addLayout(horizontal_layout)
        self.data_tab.setLayout(layout)

    def create_column_selection_group(self):
        group = QGroupBox("Column Selection")
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        left_column_layout = QVBoxLayout()
        self.input_selector = QListWidget()
        self.input_selector.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.input_selector.setToolTip("Select the columns that will be used as input features for the model.")
        left_column_layout.addWidget(QLabel("Features:"))
        left_column_layout.addWidget(self.input_selector)

        right_column_layout = QVBoxLayout()
        self.output_selector = QListWidget()
        self.output_selector.setToolTip("Select the column that will be used as the target variable.")
        right_column_layout.addWidget(QLabel("Target:"))
        right_column_layout.addWidget(self.output_selector)

        self.confirm_button = QPushButton("Confirm Selection ⮕")
        self.confirm_button.setFixedHeight(40)
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

        self.confirm_button.setToolTip("Confirms the selected columns as input and output characteristics.")
        self.confirm_button.clicked.connect(self.confirm_selection)

        layout.addLayout(left_column_layout)
        layout.addLayout(right_column_layout)
        layout.addWidget(self.confirm_button)

        layout.setStretchFactor(left_column_layout, 1)
        layout.setStretchFactor(right_column_layout, 1)

        group.setLayout(layout)
        return group


    def create_preprocess_group(self):
        group = QGroupBox("Preprocessing Options")
        layout = QVBoxLayout()

        self.error_label = QLabel("No empty values detected.\nProceed to the next step.")
        self.error_label.setStyleSheet("""
            color: #333;
            font-weight: semi-bold;
            font-size: 15px;
            font-family: 'Bahnschrift';
            padding: 5px; 
            border-radius: 5px;                                        
            background-color: #e0e0e0;
        """)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.error_label.setVisible(False)

        self.nan_options = QComboBox()
        self.nan_options.setFixedWidth(200)
        self.nan_options.setToolTip("Select an option to handle missing values ​​(NaN) in the dataset.")
        self.nan_options.addItems([
            "Select Option",
            "Remove rows with NaN",
            "Fill NaN with Mean",
            "Fill NaN with Median",
            "Fill NaN with Constant"
        ])

        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Enter constant value")
        self.constant_input.setToolTip("Enter a constant value to replace the NaN values ​​in the columns.")
        self.constant_input.setFixedWidth(200)
        self.constant_input.setDisabled(True)

        self.apply_button = QPushButton("Apply Preprocessing ⮕")
        self.apply_button.setFixedSize(200,40)  
        self.apply_button.setToolTip("Applies selected preprocessing options for NaN values.")

        layout.addWidget(self.error_label)
        layout.addWidget(self.nan_options)
        layout.addWidget(self.constant_input)
        layout.addWidget(self.apply_button)
        group.setLayout(layout)
        return group

    def create_model_group(self):
        group = QGroupBox("Create Model")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.model_group.setFixedWidth(300)

        self.description = QTextEdit()
        self.description.setPlaceholderText("Create description")
        self.description.setFixedWidth(280)

        self.model_button = QPushButton("Create Model ⮕")
        self.model_button.setToolTip("Create a regression model based on the data and selected columns.")
        self.model_button.setFixedSize(200,40)  

        layout.addWidget(self.description)
        layout.addWidget(self.model_button)
        group.setLayout(layout)
        return group