import sys
import pandas as pd
import sqlite3
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel,
                             QHBoxLayout, QVBoxLayout, QWidget, QFileDialog,
                             QTableView, QRadioButton, QMessageBox, QAbstractScrollArea,
                             QHeaderView, QSizePolicy, QComboBox, QLineEdit,
                             QGroupBox, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QFont, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Preprocessing Dataset")
        self.setGeometry(100, 100, 800, 600)
        self.setFont(QFont("Bahnschrift", 12))
        self.data = None  # Atributo para almacenar los datos cargados
        self.input_columns = []  # Atributo para almacenar columnas de entrada
        self.output_column = None  # Atributo para almacenar la columna de salida

        # Layout principal
        main_layout = QVBoxLayout()

        # CABECERA
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("background-color: #0b5394;")
        header_widget.setFixedHeight(45)

        # Etiqueta de título
        title_label = QLabel("LINEAR REGRESSION APP")
        title_label.setFont(QFont("Bahnschrift", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white; padding-left: 0px;")
        header_layout.addWidget(title_label)

        # Espacio expansivo antes del botón
        header_layout.addStretch()

        # Botón de "UPLOAD FILE"
        self.upload_button = QPushButton("UPLOAD FILE")
        self.upload_button.setFixedHeight(28)
        self.upload_button.setFixedWidth(170)
        self.upload_button.setStyleSheet(""" 
            QPushButton {
                background-color: #F6BE00; 
                color: #0B1E3E;
                border-radius: 14px;
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

        # Etiqueta para mostrar el archivo seleccionado
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #F6BE00; padding-left: 10px;")
        self.file_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        header_layout.addWidget(self.file_label)

        # Añadir la cabecera al layout principal
        main_layout.addWidget(header_widget)

        # Crear layout horizontal para colocar Column Selection y Preprocessing Options
        horizontal_layout = QHBoxLayout()

        # Caja para las opciones de preprocesamiento
        preprocess_group = QGroupBox("Preprocessing Options")
        preprocess_layout = QVBoxLayout()

        # Combobox para seleccionar la opción de manejo de NaN
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

        # Campo de texto para valor constante
        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Enter constant value")
        self.constant_input.setFixedWidth(200)
        self.constant_input.setDisabled(True)
        preprocess_layout.addWidget(self.constant_input)

        # Cambiar disponibilidad del input de constante según la opción seleccionada
        self.nan_options.currentIndexChanged.connect(self.toggle_constant_input)

        # Botón de aplicar preprocesado
        self.apply_button = QPushButton("Apply Preprocessing")
        self.apply_button.clicked.connect(self.apply_preprocessing)
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
        preprocess_group.setLayout(preprocess_layout)

        # Sección para la selección de columnas
        column_selection_group = QGroupBox("Column Selection")
        column_selection_layout = QVBoxLayout()

        # ComboBox para seleccionar el tipo de regresión (Simple o Múltiple)
        self.simple_radio = QRadioButton("Simple")
        self.multiple_radio = QRadioButton("Multiple")
        
        # Añadir las casillas al layout de selección de columnas
        regression_type_layout = QHBoxLayout()
        regression_type_layout.addWidget(QLabel("Choose Regression Type:"))
        regression_type_layout.addWidget(self.simple_radio)
        regression_type_layout.addWidget(self.multiple_radio)
        column_selection_layout.addLayout(regression_type_layout)

        # Selector para columnas de entrada (features) que cambia según el tipo de regresión
        self.input_selector = QListWidget()  # Cambiamos a QListWidget para selección múltiple
        
        column_selection_layout.addWidget(QLabel("Select Input Columns (features):"))
        column_selection_layout.addWidget(self.input_selector)

        # Selector único para la columna de salida (target)
        self.output_selector = QComboBox()
        column_selection_layout.addWidget(QLabel("Select Output Column (target):"))
        column_selection_layout.addWidget(self.output_selector)

        # Botón para confirmar selección
        self.confirm_button = QPushButton("Confirm Selection")
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.confirm_button.setFixedHeight(40)  # Ajusta la altura
        self.confirm_button.setFixedWidth(200)  # Ajusta el ancho
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
        column_selection_layout.addWidget(self.confirm_button)

        # Agregar el layout de selección de columnas al grupo
        column_selection_group.setLayout(column_selection_layout)

        # Añadir ambos grupos (Preprocessing y Column Selection) al layout horizontal
        horizontal_layout.addWidget(column_selection_group)  # Column Selection a la izquierda
        horizontal_layout.addWidget(preprocess_group)  # Preprocessing Options a la derecha

        # Añadir el layout horizontal al layout principal
        main_layout.addLayout(horizontal_layout)

        # Configuración de la tabla para mostrar los datos
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
        main_layout.addWidget(self.table_view)

        # Contenedor principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Conectar los cambios en el tipo de regresión a la actualización del selector de entrada
        self.simple_radio.toggled.connect(self.update_input_selector)
        self.multiple_radio.toggled.connect(self.update_input_selector)

    def toggle_constant_input(self):
        """ Habilitar o deshabilitar el campo de texto para la constante """
        self.constant_input.setDisabled(self.nan_options.currentIndex() != 4)

    def select_file(self):
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Dataset", "", "Admitted files (*.csv *.xlsx *.xls *.sqlite *.db)", options=options)

        if file_path:
            try:
                self.file_label.setText(f"{file_path}")
                self.data = self.data_import(file_path)  # Cargar los datos
                self.check_for_nans()  # Comprobar valores NaN
                self.show_data()  # Mostrar los datos al cargar el archivo
            except Exception as e:
                self.file_label.setText(f"Error: {str(e)}")
                self.file_label.setStyleSheet("QLabel {color: red; padding: 5px;}")

    def data_import(self, file_path):
        """ Importar los datos desde el archivo """
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
        """ Comprobar valores NaN y mostrar un mensaje """
        if self.data.isnull().values.any():
            QMessageBox.warning(self, "Warning", "Data contains NaN values!")
    
    def apply_preprocessing(self):
        """ Aplicar la opción de preprocesamiento seleccionada por el usuario """
        if self.data is None:
            QMessageBox.warning(self, "Error", "No dataset loaded.")
            return
        option = self.nan_options.currentText()

        # Aplicar el preprocesado seleccionado
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

            self.show_data()  # Mostrar los datos preprocesados
            QMessageBox.information(self, "Success", "Data preprocessing completed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during preprocessing:\n{str(e)}")

        
    def fill_with_statistic(self, data, stat_type):
        if stat_type not in ["mean", "median"]:
            raise ValueError("Invalid statistic type.")

        for column in data.columns:
            if data[column].dtype in [int, float]:  # Solo procesar columnas numéricas
                if stat_type == "mean":
                    data[column] = data[column].fillna(data[column].mean())
                elif stat_type == "median":
                    data[column] = data[column].fillna(data[column].median())
        return data

        
    def confirm_selection(self):
        """ Confirmar selección de columnas """
        if self.data is None:
            QMessageBox.warning(self, "Warning", "No data loaded!")
            return

        selected_inputs = self.input_selector.selectedItems()
        selected_output = self.output_selector.currentText()

        if not selected_inputs or not selected_output:
            QMessageBox.warning(self, "Warning", "Please select input features and output target!")
            return

        self.input_columns = [item.text() for item in selected_inputs]
        self.output_column = selected_output

        QMessageBox.information(self, "Selection Confirmed",
                                f"Input Columns: {', '.join(self.input_columns)}\nOutput Column: {self.output_column}")

        self.show_data()  # Mostrar la tabla después de confirmar la selección

    def populate_columns(self):
        """ Llenar los selectores de columnas con nombres de columnas """
        if self.data is not None:
            self.input_selector.clear()
            self.input_selector.addItems(self.data.columns.tolist())
            self.output_selector.clear()
            self.output_selector.addItems(self.data.columns.tolist())

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
    
                # Verificar si la columna es de entrada o salida
                column_name = self.data.columns[col_index]
                if column_name in self.input_columns:
                    cell_item.setBackground(input_color)
                elif column_name == self.output_column:
                    cell_item.setBackground(output_color)
    
                items.append(cell_item)
            
            model.appendRow(items)
    
        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def update_input_selector(self):
        """ Actualizar el selector de entrada según el tipo de regresión seleccionado """
        if self.simple_radio.isChecked():
            # Si es regresión simple, solo permitir una selección
            self.input_selector.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        elif self.multiple_radio.isChecked():
            # Si es regresión múltiple, permitir selección múltiple
            self.input_selector.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        
        # Limpiar la selección anterior y repoblar las columnas
        self.input_selector.clear()
        self.populate_columns()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())