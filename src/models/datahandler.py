import pandas as pd
import sqlite3

class DataHandler:
    "Class for importing data and managing them."
    def __init__(self):
        self.data = None
        self.input_columns = []
        self.output_column = None
        self.nans = False

    def import_data(self, file_path):
        """Imports data from a file and stores it in a DataFrame.
        
        Args:
            file_path (str): Path to the file to import. Can be CSV, Excel, or SQLite.
        """
        try:
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                self.data = pd.read_excel(file_path)
            elif file_path.endswith('.sqlite') or file_path.endswith('.db'):
                conn = sqlite3.connect(file_path)
                query = "SELECT name FROM sqlite_master WHERE type='table';"
                tables = pd.read_sql(query, conn)
                if tables.empty:
                    raise ValueError("No tables found in the SQLite database.")
                self.data = pd.read_sql(f"SELECT * FROM {tables.iloc[0]['name']}", conn)
            else:
                raise ValueError("Unsupported file format. Supported formats are CSV, Excel, and SQLite.")
        except Exception as e:
            raise ValueError(f"Error while importing data: {str(e)}")

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
        """Returns the numeric columns from the dataset."""
        return self.data.select_dtypes(include=["number"]).columns.tolist()

    def apply_preprocessing(self, option, constant_value=None):
        """Applies basic preprocessing to the dataset based on the provided option.
        
        Args:
            option (str): The preprocessing option to apply (e.g., "Remove rows with NaN", "Fill NaN with Mean", etc.).
            constant_value (float, optional): Constant value to fill NaN if that option is chosen.

        Returns:
            pd.DataFrame: The modified DataFrame after preprocessing.
        """
        if option == "Remove rows with NaN":
            self.data = self.data.dropna()
        elif option == "Fill NaN with Mean":
            self.data = self.fill_with_statistic("mean")
        elif option == "Fill NaN with Median":
            self.data = self.fill_with_statistic("median")
        elif option == "Fill NaN with Constant":
            if not constant_value:
                raise ValueError("Please enter a constant value.")
            if not isinstance(constant_value, (int, float)):
                raise ValueError("Constant value must be a numeric type.")
            self.data.fillna(value=float(constant_value), inplace=True)
        else:
            raise ValueError("Please select a valid option.")
        return self.data

    def fill_with_statistic(self, stat_type):
        """Fills missing values in numeric columns with the given statistic (mean or median).
        
        Args:
            stat_type (str): The type of statistic to use for filling ("mean" or "median").
        
        Returns:
            pd.DataFrame: The DataFrame with missing values filled.
        """
        if stat_type not in ["mean", "median"]:
            raise ValueError("Invalid statistic type.")

        for column in self.data.select_dtypes(include=["number"]).columns:
            self.data[column].fillna(self.data[column].agg(stat_type), inplace=True)
        return self.data
