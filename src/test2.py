import unittest
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from unittest.mock import patch
from main import MainWindow  
import pandas as pd

class TestMainWindow(unittest.TestCase):
   
    @patch.object(MainWindow, 'check_for_nans')
    def setUp(self, mock_check_for_nans):
        """ Method that runs before each test to set up the window environment."""
        # We use a real test file for loading.
        self.test_file = "src/housing.csv"
        
        # Check if the test file exists.
        self.assertTrue(os.path.exists(self.test_file), f"The file {self.test_file} does not exist.")
        
        # Create the application and the main window.
        self.app = QApplication([])  
        self.window = MainWindow()   
        
        # Select the file (simulating that it has been loaded).
        with patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName', return_value=(self.test_file, '')):
            self.window.select_file()  

    def test_select_file_real(self):
        """ Test to check that the file loads correctly """
        # Verify that the data has been loaded correctly.
        self.assertEqual(self.window.data.shape[0], 20640)  # Verify the number of rows.
        self.assertEqual(self.window.data.shape[1], 10)     # Verify the number of columns.
        
        # Verify that some columns from the dataset are present
        self.assertTrue('housing_median_age' in self.window.data.columns)
        self.assertTrue('median_income' in self.window.data.columns)
        
        # Verify that the data is correct.
        self.assertEqual(self.window.data.loc[0, 'latitude'], 37.88)  # Verify the value of 'latitude'
        
        # Verify that the label text is the correct file name
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
        self.app = QApplication([])  
        self.window = MainWindow()   
        self.model_file = "src/test1.joblib"

        with patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName', return_value=(self.model_file, '')):
            self.window.load_model(show_window = False)

        mock_msg_box.assert_called_once_with(self.window, "Successful load", "The model has been successfully loaded.")

if __name__ == '__main__':
    unittest.main()
