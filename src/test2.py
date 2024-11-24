import unittest
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from unittest.mock import patch
from main import MainWindow  # Cambia el nombre si tu clase o archivo tiene otro nombre
import pandas as pd

class TestMainWindow(unittest.TestCase):
   
    @patch.object(MainWindow, 'check_for_nans')
    def setUp(self, mock_check_for_nans):
        """ Método que se ejecuta antes de cada test para configurar el entorno de la ventana """
        # Usamos un archivo de prueba real para la carga
        self.test_file = "src/housing.csv"
        
        # Verificar si el archivo de prueba existe
        self.assertTrue(os.path.exists(self.test_file), f"El archivo {self.test_file} no existe.")
        
        # Crear la aplicación y la ventana principal
        self.app = QApplication([])  # Crear la aplicación Qt
        self.window = MainWindow()   # Crear la ventana principal
        
        # Seleccionar el archivo (simulando que se ha cargado)
        with patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName', return_value=(self.test_file, '')):
            self.window.select_file()  # Este método cargará el archivo

    def test_select_file_real(self):
        """ Test para comprobar que se carga correctamente el archivo """
        # Verificar que los datos se han cargado correctamente
        self.assertEqual(self.window.data.shape[0], 20640)  # Verifica el número de filas
        self.assertEqual(self.window.data.shape[1], 10)     # Verifica el número de columnas
        
        # Verificar que algunas columnas del conjunto de datos están presentes
        self.assertTrue('housing_median_age' in self.window.data.columns)
        self.assertTrue('median_income' in self.window.data.columns)
        
        # Verificar que los datos son correctos
        self.assertEqual(self.window.data.loc[0, 'latitude'], 37.88)  # Verifica el valor de 'latitude'
        
        # Verificar que el texto de la etiqueta es el nombre correcto del archivo
        self.assertEqual(self.window.file_label.text(), self.test_file)
"""
    @patch('PyQt6.QtWidgets.QMessageBox.information') 
    def test_create_model(self, mock_information):
        # Asegurarse de que los datos fueron cargados antes de intentar crear el modelo
        self.assertEqual(self.window.data.shape[0], 20640)
        self.assertEqual(self.window.data.shape[1], 10)
        
        # Definir las columnas de entrada y salida
        self.window.input_columns = ['housing_median_age']
        self.window.output_column = 'median_house_value'
        
        # Aplicar el preprocesamiento de NaN con la media
        self.window.nan_options.setCurrentText("Fill NaN with Mean")
        self.window.apply_preprocessing()  # Aplica el preprocesamiento

        # Verificar que los NaN fueron reemplazados por la media
        self.assertFalse(self.window.data.isnull().any().any(), "Data contains NaN values after preprocessing")

        self.window.description.setPlainText("test_description")
        # Crear el modelo usando los datos ya cargados
        self.window.create_model()  # Llama a la función para crear el modelo
"""

class TestModel(unittest.TestCase):
    @patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName')
    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_open_model(self, mock_msg_box, mock_get_open_file):
        self.app = QApplication([])  # Crear la aplicación Qt
        self.window = MainWindow()   # Crear la ventana principal
        self.model_file = "src/test1.joblib"

        with patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName', return_value=(self.model_file, '')):
            self.window.load_model(show_window = False)

        mock_msg_box.assert_called_once_with(self.window, "Carga Exitosa", "El modelo se ha cargado exitosamente.")

if __name__ == '__main__':
    unittest.main()
