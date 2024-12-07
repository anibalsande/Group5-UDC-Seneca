import sys
import pandas as pd
import sqlite3
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import joblib
from sklearn.linear_model import LinearRegression

#Modules
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

        # Configuración de la tabla para mostrar los datos
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

        # Primera columna (Texto y Multiselector)
        left_column_layout = QVBoxLayout()
        
        # Features (primera columna)
        self.input_selector = QListWidget()  # Cambiamos a QListWidget para selección múltiple
        self.input_selector.setSelectionMode(QListWidget.SelectionMode.MultiSelection)  
        self.input_selector.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        left_column_layout.addWidget(QLabel("Features:"))
        left_column_layout.addWidget(self.input_selector)
        self.input_selector.setToolTip("Select the columns that will be used as input features for the model.")


        # Segunda columna (Texto, Dropdown)
        right_column_layout = QVBoxLayout()
        target_label = QLabel("Target:")
        target_label.setToolTip("The 'Target' is the dependent variable column we aim to predict.")
        right_column_layout.addWidget(target_label)

        self.output_selector = QListWidget()
        self.output_selector.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)    
        self.output_selector.setToolTip("Select the column that will be used as the target variable.")
        right_column_layout.addWidget(self.output_selector)

        # Confirm button (segunda columna)
        self.confirm_button = QPushButton("Confirm Selection ⮕")
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.confirm_button.setFixedHeight(40)  # Ajusta la altura
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

        # Agregar las dos columnas al layout principal
        column_selection_layout.addLayout(left_column_layout)
        column_selection_layout.addLayout(right_column_layout)
        column_selection_layout.addWidget(self.confirm_button)
        column_selection_layout.setAlignment(self.confirm_button, Qt.AlignmentFlag.AlignBottom)

        column_selection_layout.setStretchFactor(left_column_layout, 1)
        column_selection_layout.setStretchFactor(right_column_layout, 1)  

        # Agregar el layout principal al grupo
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
        self.apply_button.setFixedHeight(40)  # Ajusta la altura
        self.apply_button.setFixedWidth(200)  # Ajusta el ancho
        self.apply_button.setToolTip("Applies selected preprocessing options for NaN values.")
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
        self.model_button.setFixedHeight(40)  # Ajusta la altura
        self.model_button.setFixedWidth(200)  # Ajusta el ancho
        self.model_button.setToolTip("Create a regression model based on the data and selected columns.")
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
        horizontal_layout.addWidget(self.column_selection_group)  # Column Selection a la izquierda
        horizontal_layout.addWidget(self.preprocess_group)  # Preprocessing Options al centro
        horizontal_layout.addWidget(self.model_group)  # Model

        # Añadir el layout horizontal al layout principal
        main_layout.addLayout(horizontal_layout)

        # Contenedor principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Conectar los cambios en el tipo de regresión a la actualización del selector de entrada
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
                self.data = self.data_import(file_path)  # Cargar los datos
                self.welcome_label.setText("Showing Data...")
                self.check_for_nans()  # Comprobar valores NaN
                self.input_columns = []  # Atributo para almacenar columnas de entrada
                self.output_column = None
                self.show_data()  # Mostrar los datos al cargar el archivo
                self.populate_columns()
                self.table_widget.setCurrentWidget(self.table_view)
                self.column_selection_group.setEnabled(True)
                self.preprocess_group.setEnabled(False)
                self.model_group.setEnabled(False)

            except Exception as e:
                self.file_label.setText(f"Error: {str(e)}")
                self.file_label.setStyleSheet("QLabel {color: red; padding: 5px;}")
        else:
            self.welcome_label.setText("No file was selected. \nPlease import database or an existing model.")
            

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
        """Check for NaN or empty values in the DataFrame and display a message to the user."""
        if self.data is not None:
            # Summary of NaN values per column
            nan_summary = self.data.isnull().sum()

            # Filter columns that contain NaN values
            nan_columns = nan_summary[nan_summary > 0]

            if not nan_columns.empty:
                # Construir la lista con la información de las columnas, usando <br> para saltos de línea
                columns_info = '<br>'.join(f"{col}: {count}" for col, count in nan_columns.items())
                
                # Mostrar el mensaje con formato HTML para incluir la línea horizontal
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
            self.model_group.setEnabled(True)
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

    def populate_columns(self):
        """ Llenar los selectores de columnas con nombres de columnas numéricas """
        if self.data is not None:
            numeric_columns = self.data.select_dtypes(include=["number"]).columns.tolist()
            self.input_selector.clear()
            self.input_selector.addItems(numeric_columns)
            self.output_selector.clear()
            self.output_selector.addItems(numeric_columns)

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

    def update_output_selector(self):
        selected_inputs = [item.text() for item in self.input_selector.selectedItems()]
        numeric_columns = self.data.select_dtypes(include=["number"]).columns
        remaining_columns = [col for col in numeric_columns if col not in selected_inputs]
        
        self.output_selector.clear()
        self.output_selector.addItems(remaining_columns)

    def create_model(self):
        description_text = self.description.toPlainText().strip()
        # Verificar si la descripción está vacía
        if not description_text:
            response = QMessageBox.question(
                self, "Empty Description",
                "The model description is empty. Do you want to proceed without a description?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            # Si el usuario elige "No", detenemos el proceso para que modifique la descripción
            if response == QMessageBox.StandardButton.No:
                return  # Salir de la función sin continuar

        # Asignar la descripción final después de la decisión del usuario
        self.model_description = description_text or "No description provided"

        # Crear una instancia de ModelTrainer y llamar a su método para entrenar y mostrar los resultados
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
        # Diálogo para seleccionar el archivo
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Cargar Modelo",
            "",
            "Joblib (*.joblib);;Pickle (*.pkl);;All Files (*)"
        )

        if file_path:
            try:
                # Cargar el modelo guardado
                model_info = joblib.load(file_path)

                # Extraer información del modelo
                description = model_info.get('description', 'Sin descripción')
                coefficients = model_info.get('coefficients', [])
                intercept = model_info.get('intercept', 0)
                metrics = model_info.get('metrics', {})
                r2 = metrics.get('R²', 'N/A')
                mse = metrics.get('MSE', 'N/A')
                formula = model_info.get('formula', 'N/A')
                input_columns = model_info.get('input_columns', [])
                output_column = model_info.get('output_column', '')

                # Crear el modelo de regresión lineal utilizando los coeficientes e intercepto del modelo cargado
                model = LinearRegression()
                model.coef_ = coefficients
                model.intercept_ = intercept

                # Preparar datos para la gráfica (esto se puede modificar según tus necesidades)
                plot_data = None  # Aquí puedes definir datos para graficar si es necesario

                # Pasar los datos a ResultsWindow con los parámetros correctos
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
                QMessageBox.critical(self, "Error", f"No se pudo cargar el modelo:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # Aplicar el estilo CSS correctamente
    app.setStyleSheet("""
        QMainWindow {
            background-color: #0b5394;
        }

        QTabWidget::tab-bar {
            alignment: center;
        }

        QTabBar::tab:selected {
            background: #073763; /* Fondo para la pestaña activa */
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
            background: white; /* Fondo blanco para el contenido de las pestañas */
        }

        /* Estilo para las pestañas deshabilitadas */
        QTabBar::tab:disabled {
            background: #d3d3d3;  /* Fondo gris claro */
            color: #a9a9a9;  /* Texto gris claro */
        }
                         
        QMessageBox {
        color: #0A4B85;  /* Texto en azul oscuro */
        }
    """)

    window.show()
    sys.exit(app.exec())