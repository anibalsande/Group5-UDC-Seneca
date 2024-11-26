from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)  # Set margins to 0
        self.steps_text = [
            "1. **Select Your Dataset**\n\nThe first step is to select the dataset...",
            "2. **Selecting Variables**\n\nAfter you open a dataset, its columns...",
            "3. **Data Preprocessing**\n\nBefore creating a model, you must handle missing or unreadable values...",
            "4. **Model Creation and Prediction**\n\nTo create your model: Name your model...",
            "5. **Saving and Loading Models**\n\nTo save a model, from the Model Results window..."
        ]
        self.steps_titles = [
            "SELECT YOUR DATASET",
            "SELECTING VARIABLES",
            "DATA PREPROCESSING",
            "MODEL CREATION",
            "SAVING & LOADING"
        ]
        self.current_step = 0  # Tracks the current step
        self.ui()  # Call the function to set up the UI

    def ui(self):
        # Main layout (vertical layout)
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

        # Tab buttons area
        tabs_widget = QWidget()
        tabs_layout = QHBoxLayout()
        tabs_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tabs_widget.setLayout(tabs_layout)

        # Create tab buttons
        self.tab_buttons = []
        for i, title in enumerate(self.steps_titles):
            button = QPushButton(title)
            button.setFixedSize(200, 40)
            button.setStyleSheet(self.get_tab_style(i))  # Apply style based on state
            button.clicked.connect(self.update_step(i))
            self.tab_buttons.append(button)
            tabs_layout.addWidget(button)

        # Description area
        self.description_label = QLabel(self.steps_text[self.current_step])
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("color: black; font-size: 14px; padding: 10px;")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add widgets to main layout
        layout.addWidget(header_widget)
        layout.addWidget(tabs_widget) 
        layout.addWidget(self.description_label)

        # Set the layout
        self.setLayout(layout)

    def get_tab_style(self, index):
        """Return style for a tab based on its state."""
        if index < self.current_step:
            # Past steps (blue and completed)
            return """
                background-color: #0b5394;  /* Blue */
                color: white;
                font-weight: bold;
                border: none;
                border-bottom: 2px solid #073763;
            """
        elif index == self.current_step:
            # Current step (yellow highlight)
            return """
                background-color: #ffd966;  /* Yellow */
                color: black;
                font-weight: bold;
                border: none;
                border-bottom: 2px solid #f1c232;
            """
        else:
            # Future steps (gray and inactive)
            return """
                background-color: #f0f0f0;
                color: #b0b0b0;
                font-weight: normal;
                border: none;
                border-bottom: 2px solid #d0d0d0;
            """

    def update_step(self, step_index):
        """Return a lambda function to update the current step."""
        return lambda: self.set_current_step(step_index)

    def set_current_step(self, step_index):
        """Update the current step and refresh styles."""
        self.current_step = step_index
        self.description_label.setText(self.steps_text[self.current_step])
        # Update tab styles
        for i, button in enumerate(self.tab_buttons):
            button.setStyleSheet(self.get_tab_style(i))
