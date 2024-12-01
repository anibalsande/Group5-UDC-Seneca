from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)  # Set margins to 0
        self.steps_text = [
            """<b>The first step is to select the dataset for your model.</b> 
            The LRM App can utilize data in <i>.csv</i> format, <i>Excel</i> spreadsheets, or <i>SQLite</i> databases.

            <b>To select dataset:</b>
            <ul>
                <li>Select <b>Open File</b>.</li>
                <li>Navigate to your dataset file.</li>
                <li>Double-click the file or select it and then select <b>Open</b>.</li>
            </ul>

            <i>Note:</i> If any <b>NaN</b> items are detected, a dialog box opens to inform you. Select <b>OK</b> to continue.
            """,

            """<b>After you open a dataset, its columns will appear under the Features and Target menus in the Column Selection panel.</b> 
            You can select single or multiple independent variables for your Feature(s). You can only select one dependent variable for the Target.

            <i>Note:</i> The LRM App can provide the model metrics and equation for a multiple-independent-variable linear regression but cannot graph it. 
            The LRM App can only display a graph for a <b>single-independent-variable</b> or simple linear regression.

            <b>To select variables:</b>
            <ul>
                <li>Scroll through the column headings in the <b>Features</b> menu.</li>
                <li>Select a desired <b>Feature(s)</b> by clicking on it or them. A vertical bar appears beside the <b>Feature(s)</b> selected.</li>
                <li>To deselect a Feature, click it again. The vertical bar disappears.</li>
                <li>Repeat the selection process with the column headings in the <b>Target</b> menu.</li>
                <li>Select <b>Confirm Selection</b>. The Selection Confirmed dialog box opens to summarize your choices for Input Columns (Features) and Output Column (Target).</li>
                <li>Select <b>OK</b>.</li>
            </ul>
            """,

            """<b>Before you can create a model, you must remove or fill in missing or unreadable values ("NaN" or "Not a Number" values) in the dataset.</b>

            <b>To preprocess data:</b>
            <ul>
                <li>Open the menu under <b>Preprocessing Options</b> by selecting the down arrow.</li>
                <li>Select the appropriate option (remove or fill with the <i>mean</i>, <i>median</i>, or a constant) for the NaNs in your dataset.</li>
                <li>If you select <b>Fill NaN with a Constant</b>, enter the constant in the field labelled "<b>Enter constant value</b>".</li>
                <li>Select <b>Apply Preprocessing</b>. A <i>Success</i> message appears to confirm preprocessing.</li>
                <li>Select <b>OK</b>.</li>
            </ul>
            """,

            """<b>You are ready to create your model, view the metrics, and make predictions.</b>

            <b>To create model and view metrics:</b>
            <ul>
                <li>Name your model in the <b>Create description</b> field. <i>Note:</i> You can create a model with no name. A dialog box appears asking if you are sure before you can continue. You can still save the model.</li>
                <li>Select <b>Create model</b>. The model results appear in the Display Area under the Model tab. The Model Metrics box shows the name, coefficient of determination, mean squared error, and model formula.</li>
                <li>For a simple (single-independent-variable) linear regression, the model results also display a graph. 
                <i>Note:</i> No graph appears for a multiple linear regression.</li>
            </ul>

            <b>To make a prediction:</b>
            <ul>
                <li>In the <b>Make a Prediction</b> panel, enter the Feature value you wish to use to make a prediction.</li>
                <li>Select <b>Make Prediction</b>. The predicted Target value appears in the <b>Prediction</b> field.</li>
            </ul>
            """,

            """<b>After creating your model, you can save it from the Model tab and reload it at a later time.</b>

            <b>To save a model:</b>
            <ul>
                <li>From the Model tab, select <b>Save model</b>.</li>
                <li>Navigate to the location where you want to save.</li>
                <li>Enter your desired file name and select <b>Save</b>. The file saves with a .joblib extension, and a dialog box appears to inform you of the successful save.</li>
                <li>Select <b>OK</b>.</li>
            </ul>

            <b>To reload a model:</b>
            <ul>
                <li>From the Data tab, select <b>Open Model</b>.</li>
                <li>Navigate to the location of your saved model's .joblib file.</li>
                <li>Double-click the file or select it and select <b>Open</b>. A dialog box opens to inform you the model has been loaded successfully.</li>
                <li>Select <b>OK</b>.</li>
            </ul>
            """,
        ]

        self.steps_titles = [
            "SELECT YOUR DATASET",
            "SELECTING VARIABLES",
            "DATA PREPROCESSING",
            "CREATE AND VIEW MODEL",
            "SAVING AND LOADING MODELS"
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
        self.description_label.setStyleSheet("color: black; font-family: 'Open Sans'; font-weight: 500; font-size: 15px; padding: 10px; margin-left: 10px; margin-right: 10px;")
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
            # Past steps (blue = completed)
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
