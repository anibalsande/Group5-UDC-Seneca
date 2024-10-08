import sqlite3
import pandas as pd

def dataimport(file):
    extension = file.split('.')[-1].lower()
    
    if extension == "csv":
        datos = pd.read_csv(file)
        if datos.empty:
                raise ValueError("El archivo CSV está vacío.")
        print("Archivo CSV cargado correctamente.")

    elif extension in ["xlsx", "xls"]:
            datos = pd.read_excel(file)
            datos = pd.read_excel(file)
            if datos.empty:
                raise ValueError("El archivo Excel está vacío.")
            print("Archivo Excel cargado correctamente.")


    elif extension in ["sqlite", "db"]:
            connection = sqlite3.connect(file)
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            cursor = connection.cursor()
            cursor.execute(query)
            tablas = cursor.fetchall()
            if len(tablas) == 0:
                raise ValueError("No se encontraron tablas en la base de datos.")
            tabla = tablas[0][0]
            datos = pd.read_sql_query(f"SELECT * FROM {tabla}", connection)
            connection.close()
            print("Base de datos SQLite cargada correctamente.")

    else:
            raise ValueError("Formato de file no soportado.")
        
    # Previsualizar las primeras filas
    print("Previsualización de los datos:")
    print(datos.head())  # Muestra las primeras 5 filas
        
    return datos

file = 'housing.db'
datos = dataimport(file)