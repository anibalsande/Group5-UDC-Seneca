import unittest
import os
from PyQt6.QtWidgets import QApplication
from unittest.mock import patch
from main import MainWindow  # Cambia el nombre si tu clase o archivo tiene otro nombre
import pandas as pd

class TestMainWindow(unittest.TestCase):

    @patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName', return_value=("src/housing.csv", ''))
    @patch.object(MainWindow, 'check_for_nans')
    def test_select_file_real(self, mock_get_open_file_name, mock_check_for_nans):
        # Using a real "test" file instead of a mock
        test_file = "src/housing.csv"

        # Checks if file exists
        self.assertTrue(os.path.exists(test_file), f"File {test_file} doesn't exist.")

        # Create the app
        app = QApplication([])
        self.window = MainWindow()

        # Select file with our chosen test file 
        self.window.select_file()

        # Check if rows and columns were correctly imported
        self.assertEqual(self.window.data.shape[0], 20640)
        self.assertEqual(self.window.data.shape[1], 10) 

        # Check if some columns from the dataset were correctly imported 
        self.assertTrue('housing_median_age' in self.window.data.columns)  # Verifica que 'col1' está en las columnas
        self.assertTrue('median_income' in self.window.data.columns)  # Verifica que 'col2' está en las columnas

        # Check if data is correct
        self.assertEqual(self.window.data.loc[0, 'latitude'], 37.88)

        # Make sure file label is correct 
        self.assertEqual(self.window.file_label.text(), test_file)

    @patch.object(MainWindow, 'create_model')
    def test_create_model(self, mock_create_model):        
        # Check if data has been uploaded before
        self.assertEqual(self.window.data.shape[0], 20640) 
        self.assertEqual(self.window.data.shape[1], 10)

        self.window.input_columns = ['housing_median_age']
        self.window.output_column = 'median_house_value'

        self.window.nan_options.setCurrentText("Fill NaN with Mean")
        self.window.apply_preprocessing()

        # Crear el modelo usando los datos ya cargados
        self.window.create_model()

        # Check if model is not empty
        self.assertIsNotNone(self.window.model)

        # Verificar que el modelo prediga correctamente (por ejemplo, con la primera fila de datos)
        X_test = self.window.data[self.window.input_columns].iloc[0:1]  # Primera fila de datos
        y_pred = self.window.model.predict(X_test)
        self.assertEqual(len(y_pred), 1)  # Asegúrate de que haya una predicción para esa fila


if __name__ == '__main__':
    unittest.main()
