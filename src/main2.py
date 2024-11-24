import sys
import pandas as pd
import sqlite3
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import joblib
from sklearn.linear_model import LinearRegression

from handle_data import DataProcessor
from model_results import ModelTrainer,ResultsWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preprocessing Dataset")
        self.setGeometry(100, 100, 800, 600)
        #self.setStyleSheet("background-color: white;")
        self.setFont(QFont("Bahnschrift", 12))

        self.data_processor = DataProcessor()  # Instancia de DataProcessor
        self.model_description = ""

        self.init_ui()  # Llamada al método para inicializar la interfaz gráfica

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Blue header
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("background-color: #0b5394;")
        header_widget.setFixedHeight(45)

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
        self.file_label.setStyleSheet("color: white; padding-left: 10px;")
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

        # Middle layout
        horizontal_layout = QHBoxLayout()

        # Configuración de la tabla para mostrar los datos
        self.table_view = QTableView()
        self.table_view.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table_view.setFixedHeight(440)
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
        main_layout.addWidget(self.table_view)

        # Column selection side
        column_selection_group = QGroupBox("Column Selection")
        column_selection_layout = QHBoxLayout()  # Cambiado a QHBoxLayout para dos columnas

        # Primera columna (Texto y Multiselector)
        left_column_layout = QVBoxLayout()
        left_column_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Features (primera columna)
        self.input_selector = QListWidget()  # Cambiamos a QListWidget para selección múltiple
        self.input_selector.setSelectionMode(QListWidget.SelectionMode.MultiSelection)  
        self.input_selector.setFixedHeight(70) 
        self.input_selector.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)     
        left_column_layout.addWidget(QLabel("Features:"))
        left_column_layout.addWidget(self.input_selector)

        # Segunda columna (Texto, Dropdown y Botón)
        right_column_layout = QVBoxLayout()
        right_column_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # Target (segunda columna)
        self.output_selector = QListWidget()
        self.output_selector.setFixedHeight(70) 
        self.output_selector.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)     
        
        target_label = QLabel("Target:")
        target_label.setToolTip("The 'Target' is the dependent variable column we aim to predict.")
        right_column_layout.addWidget(target_label)
        
        right_column_layout.addWidget(self.output_selector)

        # Confirm button (segunda columna)
        self.confirm_button = QPushButton("Confirm Selection ⮕")
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.confirm_button.setFixedHeight(40)  # Ajusta la altura
        self.confirm_button.setStyleSheet(""" 
            QPushButton {
                background-color: #0B1E3E; 
                color: white;
                padding: 10px;
                border-radius: 5px;  /* Cambiado para ser similar */
                font-weight: bold;  /* Cambiado para ser similar */
                font-size: 12px;  /* Cambiado para ser similar */
            }
            QPushButton:hover {
                background-color: #F6BE00;
                color: #0B1E3E;
            }
        """)

        # Agregar las dos columnas al layout principal
        column_selection_layout.addLayout(left_column_layout)
        column_selection_layout.addLayout(right_column_layout)
        column_selection_layout.addWidget(self.confirm_button)

        # Agregar el layout principal al grupo
        column_selection_group.setLayout(column_selection_layout)

        # Preprocess side
        self.preprocess_group = QGroupBox("Preprocessing Options")
        preprocess_layout = QVBoxLayout()
        self.preprocess_group.setFixedWidth(220)
        preprocess_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
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

        # Input constant
        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Enter constant value")
        self.constant_input.setFixedWidth(200)
        self.constant_input.setDisabled(True)
        preprocess_layout.addWidget(self.constant_input)

        # Enable constant input
        self.nan_options.currentIndexChanged.connect(self.toggle_constant_input)

        # Preprocessing button
        self.apply_button = QPushButton("Apply Preprocessing ⮕")
        self.apply_button.clicked.connect(self.data_processor.apply_preprocessing)
        self.apply_button.setFixedHeight(40)  # Ajusta la altura
        self.apply_button.setFixedWidth(200)  # Ajusta el ancho
        self.apply_button.setStyleSheet(""" 
            QPushButton {
                background-color: #0B1E3E; 
                color: white;
                padding: 10px;
                border-radius: 5px;  /* Cambiado para ser similar */
                font-weight: bold;  /* Cambiado para ser similar */
                font-size: 12px;  /* Cambiado para ser similar */
            }
            QPushButton:hover {
                background-color: #F6BE00;
                color: #0B1E3E;
            }
        """)
        preprocess_layout.addWidget(self.apply_button)

        # Configurar y agregar el layout de preprocesamiento a su grupo
        self.preprocess_group.setLayout(preprocess_layout)

        # Model side
        self.model_group = QGroupBox("Create model")
        model_layout = QVBoxLayout()
        self.model_group.setFixedWidth(300)
        self.model_group.setEnabled(False)

        self.description = QTextEdit()
        self.description.setPlaceholderText("Create description")
        self.description.setFixedWidth(260)
        self.description.setFixedHeight(40)
        model_layout.addWidget(self.description)

        # Preprocessing button
        self.model_button = QPushButton("Create model ⮕")
        self.model_button.setFixedHeight(40)  # Ajusta la altura
        self.model_button.setFixedWidth(200)  # Ajusta el ancho
        self.model_button.setStyleSheet(""" 
            QPushButton {
                background-color: #0B1E3E; 
                color: white;
                padding: 10px;
                border-radius: 5px;  /* Cambiado para ser similar */
                font-weight: bold;  /* Cambiado para ser similar */
                font-size: 12px;  /* Cambiado para ser similar */
            }
            QPushButton:hover {
                background-color: #F6BE00;
                color: #0B1E3E;
            }
        """)
        model_layout.addWidget(self.model_button)
        self.model_button.clicked.connect(self.create_model)
        
        self.model_group.setLayout(model_layout)

        # Añadir ambos grupos (Preprocessing y Column Selection) al layout horizontal
        horizontal_layout.addWidget(column_selection_group)  # Column Selection a la izquierda
        horizontal_layout.addWidget(self.preprocess_group)  # Preprocessing Options al centro
        horizontal_layout.addWidget(self.model_group)  # Model

        # Añadir el layout horizontal al layout principal
        main_layout.addLayout(horizontal_layout)

        # Contenedor principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Conectar los cambios en el tipo de regresión a la actualización del selector de entrada
        self.input_selector.itemSelectionChanged.connect(self.data_processor.update_output_selector)


    def select_file(self):
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Dataset", "", "Admitted files (*.csv *.xlsx *.xls *.sqlite *.db)", options=options)

        if file_path:
            try:
                self.file_label.setText(f"{file_path}")
                self.data_processor.data = self.data_processor.data_import(file_path)  # Uso del método del módulo preprocessor
                self.data_processor.check_for_nans()  # Comprobar NaNs con el módulo preprocessor
                self.input_columns = []  # Atributo para almacenar columnas de entrada
                self.output_column = None
                self.show_data()  # Mostrar los datos al cargar el archivo
                self.populate_columns()
            except Exception as e:
                self.file_label.setText(f"Error: {str(e)}")
                self.file_label.setStyleSheet("QLabel {color: red; padding: 5px;}")

    def toggle_constant_input(self):
        """ Habilitar o deshabilitar el campo de texto para la constante """
        self.constant_input.setDisabled(self.nan_options.currentIndex() != 4)

    def confirm_selection(self):
        """ Confirmar selección de columnas """
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
        self.show_data()  # Mostrar la tabla después de confirmar la selección
        self.preprocess_group.setEnabled(True)

    def show_data(self):
        """ Mostrar los datos en la tabla """
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(self.data.columns)

        input_color = QColor("#FFDDC1")  # Color para columnas de entrada
        output_color = QColor("#D1E8FF")  # Color para la columna de salida

        # Iterar sobre las filas de los datos
        for row in self.data.itertuples(index=False):
            items = []
            for col_index, item in enumerate(row):
                cell_item = QStandardItem(str(item))

                column_name = self.data.columns[col_index]
                if column_name in self.input_columns:
                    cell_item.setBackground(input_color)
                elif column_name == self.output_column:
                    cell_item.setBackground(output_color)

                items.append(cell_item)

            model.appendRow(items)

        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def create_model(self):
        description_text = self.description.toPlainText().strip()

        if not description_text:
            response = QMessageBox.question(self, "Empty Description",
                "The model description is empty. Do you want to proceed without a description?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if response == QMessageBox.StandardButton.No:
                return

        self.model_description = description_text or "No description provided"

        trainer = ModelTrainer(self.data, self.input_columns, self.output_column, self.model_description)

    def load_model(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Cargar Modelo", "", "Joblib (*.joblib);;Pickle (*.pkl);;All Files (*)")

        if file_path:
            try:
                model_info = joblib.load(file_path)

                description = model_info.get('description', 'Sin descripción')
                coefficients = model_info.get('coefficients', [])
                intercept = model_info.get('intercept', 0)
                metrics = model_info.get('metrics', {})
                r2 = metrics.get('R²', 0)
                # Continuar con la carga del modelo y su visualización
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading model: {str(e)}")
                
    def populate_columns(self):
        """ Llenar los selectores de columnas con las columnas del dataset """
        self.input_selector.clear()
        self.output_selector.clear()

        if self.data is not None:
            for column in self.data.columns:
                self.input_selector.addItem(column)
                self.output_selector.addItem(column)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())