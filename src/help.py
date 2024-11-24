from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)  # Set margins to 0
        self.steps = [
            ("1 ) SELECT FILE", "Open a file by clicking the 'OPEN FILE' button. This will open a file dialog to select your file."),
            ("2 ) SELECT INPUT / OUTPUT COLUMNS", "Select the column(s) you want to use as features, and a single one to predict. Only numerical columns are shown"),
            ("3 ) APPLY PREPROCESSING", "Apply preprocessing options to handle missing values or outliers. It will be applied for every column"),
            ("4 ) GENERATE MODEL", "Write a description (optional) and click 'Create model' to build the model and see the results.")
        ]
        self.ui()  # Call the function to set up the UI

    def ui(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header with instructions title
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("background-color: #0b5394; color: white;")
        header_widget.setFixedHeight(35)

        # Title in the header

        title_label = QLabel("Follow the app usage instructions")
        title_label.setStyleSheet("color: white; font-family: 'Bahnschrift'; font-size: 16px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        header_layout.addWidget(title_label)

        # Instructions area (with static text)
        instructions_widget = QWidget()
        instructions_layout = QVBoxLayout()
        instructions_widget.setLayout(instructions_layout)

        # Add each step as a box with title and description
        for step_title, step_description in self.steps:
            # Step box widget
            step_box_widget = QWidget()
            step_box_widget.setStyleSheet("""
                background-color: #f0f0f0;
                border-radius: 10px;
                margin-top: 15px;
                padding: 10px;
            """)

            # Step title and number (e.g., "STEP 1")
            step_title_label = QLabel(f"<b>{step_title}</b>")
            step_title_label.setStyleSheet("""
                color: #0B1E3E;
                font-size: 16px;
                font-weight: bold;
                padding: 5px 0;
            """)
            
            # Step description (text explaining the step)
            step_description_label = QLabel(step_description)
            step_description_label.setStyleSheet("""
                color: black;
                font-size: 12px;
                padding-left: 10px;
            """)

            # Layout for the step box
            step_layout = QVBoxLayout()
            step_layout.addWidget(step_title_label)
            step_layout.addWidget(step_description_label)
            step_box_widget.setLayout(step_layout)

            # Add the step box to the main layout
            instructions_layout.addWidget(step_box_widget)

        # Add the instructions area to the main layout
        layout.addWidget(header_widget)  # Header
        layout.addWidget(instructions_widget)  # Instructions steps

        # Set the layout for the widget
        self.setLayout(layout)
