import pandas as pd
import sqlite3

class DataHandler:
    def __init__(self):
        self.data = None
        self.input_columns = []
        self.output_column = None
        self.nans = False

    def import_data(self, file_path):
        """Load data from the specified file path."""
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            self.data = pd.read_excel(file_path)
        elif file_path.endswith('.sqlite') or file_path.endswith('.db'):
            conn = sqlite3.connect(file_path)
            query = "SELECT * FROM sqlite_master WHERE type='table';"
            tables = pd.read_sql(query, conn)
            if not tables.empty:
                table_name = tables.iloc[0]['name']
                self.data = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            else:
                raise ValueError("No tables found in the SQLite database.")
        else:
            raise ValueError("Unsupported file format.")

    def check_for_nans(self):
        """Check for missing values in the dataset and return a summary."""
        if self.data is None:
            raise ValueError("No data loaded.")

        nan_summary = self.data.isnull().sum()
        nan_columns = nan_summary[nan_summary > 0]

        if not nan_columns.empty:
            self.nans = True
            return nan_columns
        else:
            self.nans = False
            return None
        
    def get_numeric_columns(self):
        return self.data.select_dtypes(include=["number"]).columns.tolist()

    def apply_preprocessing(self, option, constant_value=None):
        if option == "Remove rows with NaN":
            self.data = self.data.dropna()
        elif option == "Fill NaN with Mean":
            self.data = self.fill_with_statistic("mean")
        elif option == "Fill NaN with Median":
            self.data = self.fill_with_statistic("median")
        elif option == "Fill NaN with Constant":
            if not constant_value:
                raise ValueError("Please enter a constant value.")
            self.data.fillna(value=float(constant_value), inplace=True)
        else:
            raise ValueError("Please select a valid option.")
        return self.data

    def fill_with_statistic(self, stat_type):
        if stat_type not in ["mean", "median"]:
            raise ValueError("Invalid statistic type.")

        for column in self.data.columns:
            if self.data[column].dtype in [int, float]:  # Only process numeric columns
                if stat_type == "mean":
                    self.data[column] = self.data[column].fillna(self.data[column].mean())
                elif stat_type == "median":
                    self.data[column] = self.data[column].fillna(self.data[column].median())
        return self.data