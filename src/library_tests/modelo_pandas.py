# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 02:49:11 2024

@author: ccarr
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Cargar los datos
file_path = 'C:/Users/ccarr/Downloads/housing.xlsx'  # Cambia la ruta por la correcta
data = pd.read_excel(file_path)

# Rellenar valores nulos en 'total_bedrooms'
 #data['total_bedrooms'].fillna(data['total_bedrooms'].median(), inplace=True)
data['total_bedrooms'] = data['total_bedrooms'].fillna(data['total_bedrooms'].median())
# Convertir variable categórica en variables dummy
data = pd.get_dummies(data, columns=['ocean_proximity'], drop_first=True)

# Definir variables independientes (X) y dependiente (y)
X = data.drop('median_house_value', axis=1)
y = data['median_house_value']

# Dividir datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Obtener predicciones en entrenamiento
y_train_pred = model.predict(X_train)

# Calcular MSE y R²
mse = mean_squared_error(y_train, y_train_pred)
r2 = r2_score(y_train, y_train_pred)

# Imprimir resultados
print(f"MSE de entrenamiento: {mse}")
print(f"R² de entrenamiento: {r2}")
