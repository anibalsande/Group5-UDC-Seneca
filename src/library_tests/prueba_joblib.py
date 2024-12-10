# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 11:51:53 2024

@author: ccarr
"""


from sklearn.linear_model import LinearRegression  
from sklearn.datasets import make_regression  
import joblib  
import numpy as np  
from sklearn.metrics import mean_squared_error  

#Generar datos de ejemplo (nº muestras, nº características, desviación del ruído en salidas y aleatoriedad)
X, y = make_regression(n_samples=100, n_features=1, noise=0.1, random_state=42)

#Creamos y entrenamos el modelo
model = LinearRegression()
model.fit(X, y) #fit ajusta el modelo a los datos

# Imprimimos los coeficientes del modelo
print(f"Coeficientes del modelo: {model.coef_}, Intercepto: {model.intercept_}")

# Evaluamos el modelo en los datos de prueba y calcular el error inicial
p_iniciales= model.predict(X)
mse_inicial = mean_squared_error(y, p_iniciales)
print(f"Error cuadrático inicial (MSE): {mse_inicial}")

#  Guardamos el modelo en un archivo
model_filename = "C:/Users/ccarr/OneDrive - Universidade da Coruña/Escritorio/IS/modelo_regresion.joblib"
joblib.dump(model, model_filename)
print(f"Modelo guardado en el archivo: {model_filename}")

# Cargamos el modelo desde el archivo
modelo_cargado = joblib.load(model_filename)
print("Modelo cargado correctamente.")

# Usamos el modelo ya cargado para hacer predicciones y calcular un nuevo MSE
predicciones = modelo_cargado.predict(X)
mse = mean_squared_error(y, predicciones)
print("Primeras 5 predicciones realizadas con el modelo cargado:", predicciones[:5])
print(f"Error cuadrático medio de las predicciones: {mse}")

# Comparar el modelo cargado con el original
assert mse_inicial == mse, "El modelo cargado no es idéntico al modelo original."
print("El modelo cargado es idéntico al modelo original.")
