import pandas as pd
import sqlite3

class DataHandler:
    def __init__(self):
        self.data = None
        self.input_columns = []
        self.output_column = None
        self.nans = False

    def load_data(self, file_path):
        """
        Carga los datos desde un archivo y verifica la presencia de NaNs.

        Args:
            file_path (str): Ruta del archivo a cargar.
        """
        # Dependiendo del tipo de archivo, se realiza la carga adecuada
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            self.data = pd.read_excel(file_path)
        elif file_path.endswith(('.sqlite', '.db')):
            conn = sqlite3.connect(file_path)
            self.data = pd.read_sql_query("SELECT * FROM table_name", conn)  # Asegúrate de especificar la tabla correcta
            conn.close()
        
        # Aquí se pueden agregar otras verificaciones, como si hay NaNs, etc.
        self.nans = self.check_for_nans()

        # Asignamos las columnas de entrada y salida
        self.populate_columns()

    def check_for_nans(self):
        """
        Verifica si hay valores NaN en los datos cargados.
        
        Returns:
            bool: True si hay NaNs, False si no los hay.
        """
        if self.data.isnull().values.any():
            return True
        return False

    def populate_columns(self):
        """
        Rellena las columnas de entrada y salida a partir de los datos cargados.
        Esto puede adaptarse a diferentes criterios dependiendo de la estructura de los datos.
        """
        if self.data is not None:
            self.input_columns = list(self.data.columns[:-1])
            self.output_column = self.data.columns[-1]