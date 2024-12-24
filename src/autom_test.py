import unittest
from unittest.mock import patch
from models.datahandler import DataHandler
from models.modelhandler import ModelHandler
import pandas as pd
import numpy as np

class TestMainWindow(unittest.TestCase):

    def test_select_file_real(self):
        """ Test to check that the file loads correctly """
        file_path = "datafiles/housing.csv"
        testmodel = DataHandler(file_path)
        # Verify that the data has been loaded correctly.
        self.assertEqual(testmodel.data.shape[0], 20640)  # Verify the number of rows.
        self.assertEqual(testmodel.data.shape[1], 10)     # Verify the number of columns.
        
        # Verify that some columns from the dataset are present
        self.assertTrue('housing_median_age' in testmodel.data.columns)
        self.assertTrue('median_income' in testmodel.data.columns)
        # Verify that the data is correct.
        self.assertEqual(testmodel.data.loc[0, 'latitude'], 37.88)  # Verify the value of 'latitude'
        
    @patch.object(DataHandler, 'import_data')  # Replaces import data
    def test_emptyvalues(self, mock_import_data):
        """ Test to check that empty values """

        data_with_nan = pd.DataFrame({
            'col1': [1, 2, np.nan, 4],
            'col2': [5, np.nan, 7, 8],
            'col3': [10, 20, np.nan, 40]})
        
        mock_import_data.return_value = None

        testmodel = DataHandler("dummy_path")
        testmodel.data = data_with_nan
        testmodel.input_columns = ['col1', 'col2']
        testmodel.output_column = 'col3'

        data_without_nan = testmodel.apply_preprocessing("Fill NaN with Mean")

        self.assertTrue(data_without_nan.isnull().sum().sum() == 0)

        expected_col1_mean = data_with_nan['col1'].mean()
        expected_col2_mean = data_with_nan['col2'].mean()
        expected_col3_mean = data_with_nan['col3'].mean()
        
        pd.testing.assert_series_equal(data_without_nan['col1'], data_with_nan['col1'].fillna(expected_col1_mean))
        pd.testing.assert_series_equal(data_without_nan['col2'], data_with_nan['col2'].fillna(expected_col2_mean))
        pd.testing.assert_series_equal(data_without_nan['col3'], data_with_nan['col3'].fillna(expected_col3_mean))

class TestModel(unittest.TestCase):
    def test_create_model(self):
        data = pd.DataFrame({
            'longitude': [-122.23, -122.22, -122.24, -122.25, -122.25, -122.25, -122.25, -122.25, -122.26, -122.25],
            'latitude': [37.88, 37.86, 37.85, 37.85, 37.85, 37.85, 37.84, 37.84, 37.84, 37.84],
            'housing_median_age': [41.0, 21.0, 52.0, 52.0, 52.0, 52.0, 52.0, 52.0, 42.0, 52.0],
            'total_rooms': [880.0, 7099.0, 1467.0, 1274.0, 1627.0, 919.0, 2535.0, 3104.0, 2555.0, 3549.0],
            'total_bedrooms': [129.0, 1106.0, 190.0, 235.0, 280.0, 213.0, 489.0, 687.0, 665.0, 707.0],
            'population': [322.0, 2401.0, 496.0, 558.0, 565.0, 413.0, 1094.0, 1157.0, 1206.0, 1551.0],
            'households': [126.0, 1138.0, 177.0, 219.0, 259.0, 193.0, 514.0, 647.0, 595.0, 714.0],
            'median_income': [8.3252, 8.3014, 7.2574, 5.6431, 3.8462, 4.0368, 3.6591, 3.1200, 2.0804, 3.6912],
            'median_house_value': [452600.0, 358500.0, 352100.0, 341300.0, 342200.0, 269700.0, 299200.0, 241400.0, 226700.0, 261100.0],
            'ocean_proximity': ['NEAR BAY'] * 10
        })

        input_columns = ['longitude', 'total_rooms']
        output_column = 'median_house_value'

        testmodel = ModelHandler()
        testmodel.train_model(data, input_columns, output_column)

        assert testmodel.metrics['R²'] > 0, "R² value should be greater than 0 indicating a good model."
        assert testmodel.metrics['MSE'] > 0, "MSE should be greater than 0 to indicate predictive ability."
        assert testmodel.coef[0] != 0, "Coefficient for 'longitude' should not be zero."
        assert testmodel.coef[1] != 0, "Coefficient for 'total_rooms' should not be zero."

if __name__ == '__main__':
    unittest.main()
