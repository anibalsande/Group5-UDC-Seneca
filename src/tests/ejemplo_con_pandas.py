import pandas as pd

# Cargar datos desde un archivo CSV
ruta_archivo = "C:/Users/ccarr/Downloads/housing.csv"  # Cambia la ruta si es necesario
datos = pd.read_csv(ruta_archivo)

# Visualizar las primeras filas 
print("Primeras filas del DataFrame:")
print(datos.head())

# Manejar valores nulos
print("\nAntes de manejar valores nulos:")
print(datos.isnull().sum())  # Mostrar cantidad de valores nulos por columna

# Rellenar los valores nulos en 'total_bedrooms' con la mediana
datos['total_bedrooms'].fillna(datos['total_bedrooms'].median(), inplace=True)

print("\nDespués de manejar valores nulos:")
print(datos.isnull().sum())  # Verificar que ya no hay valores nulos

# Seleccionar características
X = datos[['latitude', 'longitude', 'total_bedrooms']]  # Características
print("\nCaracterísticas seleccionadas:")
print(X.head())

# Calcular estadísticas descriptivas
print("\nEstadísticas descriptivas:")
print(datos.describe())
