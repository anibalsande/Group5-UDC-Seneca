# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 11:41:20 2024

@author: ccarr
"""


from sklearn.linear_model import LinearRegression  
from sklearn.datasets import make_regression  
import pickle  
import numpy as np  
from sklearn.metrics import mean_squared_error  

#  Generar datos 
X, y = make_regression(n_samples=100, n_features=1, noise=0.1, random_state=42)

# Crear el modelo y entrenarlo

model = LinearRegression()
model.fit(X, y)

# Imprimir los coeficientes del modelo

print(f"Coeficientes del modelo: {model.coef_}, Intercepto: {model.intercept_}")

#  Guardar el modelo en un archivo

model_filename = "C:/Users/ccarr/OneDrive - Universidade da Coruña/Escritorio/IS/modelo_regresion.pkl"

with open(model_filename, 'wb') as file:
    pickle.dump(model, file)  # dump() serializa el modelo y lo escribe en el archivo
print(f"Modelo guardado en el archivo: {model_filename}")

# Cargar el modelo desde el archivo

with open(model_filename, 'rb') as file:
    modelo_cargado = pickle.load(file)  # load() deserializa el modelo desde el archivo
print("Modelo cargado correctamente.")

#  Usar el modelo cargado para hacer predicciones

predicciones = modelo_cargado.predict(X)

# Mostrar las primeras 5 predicciones
print("Primeras 5 predicciones realizadas con el modelo cargado:", predicciones[:5])

# Paso 6: Calcular y mostrar el error cuadrático medio (MSE)

mse = mean_squared_error(y, predicciones)
print(f"Error cuadrático medio de las predicciones: {mse}")
