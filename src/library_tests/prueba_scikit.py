# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 12:57:40 2024

@author: ccarr
"""

import openpyxl
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score

# Ruta del archivo Excel
ruta_archivo = "C:/Users/ccarr/Downloads/housing.xlsx"  

# Cargar el archivo Excel utilizando openpyxl
wb = openpyxl.load_workbook(ruta_archivo)  
hoja = wb.active  

# Extraer los datos manualmente del archivo Excel
datos = []  
for fila in hoja.iter_rows(values_only=True):  
    datos.append(fila)

# Separar el encabezado de los datos
encabezado = datos[0]  # Guardar el encabezado de las columnas
datos = datos[1:]  # Guardar solo los datos

# Convertir los datos en matrices NumPy
X = []  # Lista para las características (variables independientes)
y = []  # Lista para las etiquetas (variable dependiente)
for fila in datos:
    # Extraer características específicas para X
    X.append([fila[0], fila[1], fila[2], fila[9]])  
    y.append(fila[8])  

# Convertir las listas a matrices NumPy
X = np.array(X)  
y = np.array(y)  

# Rellenar valores nulos en 'total_bedrooms' utilizando SimpleImputer
imputer = SimpleImputer(strategy='median')  # Inicializar el imputador con estrategia de la mediana
X[:, 2] = imputer.fit_transform(X[:, 2].reshape(-1, 1)).ravel()  # Imputar valores nulos en la columna de total_bedrooms

# Convertir la columna categórica 'ocean_proximity' en variables dummy usando OneHotEncoder
encoder = OneHotEncoder(sparse_output=False, drop='first')  # Inicializar el codificador
X_categorical = encoder.fit_transform(X[:, 3].reshape(-1, 1))  # Codificar la columna categórica y transformarla en variables dummy

# Concatenar las columnas numéricas con las categóricas
X_numeric = X[:, :3].astype(float)  
X = np.hstack((X_numeric, X_categorical))  

# Dividir los datos en conjuntos de entrenamiento y prueba
X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(X, y, test_size=0.2, random_state=42)


# Crear y entrenar el modelo de regresión lineal
modelo = LinearRegression()  # Inicializar el modelo de regresión lineal
modelo.fit(X_entrenamiento, y_entrenamiento)  # Ajustar el modelo a los datos de entrenamiento

# Obtener predicciones sobre el conjunto de entrenamiento
y_entrenamiento_pred = modelo.predict(X_entrenamiento)  # Predecir los valores de y para el conjunto de entrenamiento

# Calcular el Error Cuadrático Medio (MSE) y el coeficiente de determinación (R²)
mse = mean_squared_error(y_entrenamiento, y_entrenamiento_pred)  
r2 = r2_score(y_entrenamiento, y_entrenamiento_pred)  

# Imprimir los resultados
print(f'Error Cuadrático Medio: {mse}')  
print(f'Puntuación R²: {r2}')  
