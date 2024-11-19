# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:41:32 2024

@author: ccarr
"""

# preprocessor.py
import pandas as pd
import sqlite3
from PyQt6.QtWidgets import QMessageBox

class DataProcessor:
    def __init__(self):
        self.data = None
        self.input_columns = []
        self.output_column = None

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
        """ Check for NaN or empty values in the DataFrame and display a message to the user """
        if self.data is not None:
            nan_summary = self.data.isnull().sum()
            nan_columns = nan_summary[nan_summary > 0]
            
            if not nan_columns.empty:
                columns_info = ', '.join(nan_columns.index)
                count_info = ', '.join(f"{col}: {count}" for col, count in nan_columns.items())
                QMessageBox.warning(None, "NaN Values Detected",
                                    f"Missing (NaN) values were found in the following columns:\n\n"
                                    f"{columns_info}\n\n"
                                    f"Number of NaN values per column:\n{count_info}")
            else:
                QMessageBox.information(None, "No NaN Values Found",
                                        "The dataset does not contain any missing (NaN) values.")

    def apply_preprocessing(self, nan_option, constant_value=None):
        """ Apply the preprocessing selected """
        try:
            if nan_option == "Remove rows with NaN":
                self.data = self.data.dropna()
            elif nan_option == "Fill NaN with Mean":
                self.data = self.fill_with_statistic(self.data, "mean")
            elif nan_option == "Fill NaN with Median":
                self.data = self.fill_with_statistic(self.data, "median")
            elif nan_option == "Fill NaN with Constant" and constant_value:
                self.data.fillna(value=float(constant_value), inplace=True)
            else:
                raise ValueError("Please select a valid option.")

            return self.data  # Return processed data
        except Exception as e:
            raise ValueError(f"Error occurred during preprocessing: {str(e)}")

    def fill_with_statistic(self, data, stat_type):
        if stat_type not in ["mean", "median"]:
            raise ValueError("Invalid statistic type.")

        for column in data.columns:
            if data[column].dtype in [int, float]:  # Only process numeric columns
                if stat_type == "mean":
                    data[column] = data[column].fillna(data[column].mean())
                elif stat_type == "median":
                    data[column] = data[column].fillna(data[column].median())
        return data

    def update_output_selector(self):
        remaining_columns = [col for col in self.data.columns if col not in self.input_columns]
        return remaining_columns