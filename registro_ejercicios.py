# -*- coding: utf-8 -*-
"""Registro_Ejercicios.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rVHdtoggopoLvy_7aWzvHXo6E-mbwB4Y
"""

# Importar librerias
import pandas as pd
import streamlit as st
# Crear pie de pagina con los datos de contacto de los creadores
footer = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        z-index: 10;
        width: 100%;
        background-color: rgb(14, 17, 23);
        color: black;
        text-align: center;
    }
    .footer p {
        color: white;
    }
</style>
<div class="footer">
    <p>App desarrollada por: <br />
    Luis Fernando López Echeverri | Andres Felipe Ramirez Suarez <br />
    Contactenos: <a href="#">lulopeze@unal.edu.co</a> | <a href="#">aramirezsu@unal.edu.co</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

url_exercise = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTXXom0c0qWSJIPrIQZo_0qGxSzoM0u_xe8Cijv1ZAY"
    "bP6EKshVAtvwVV2eh5Yj1Ueio8tzb7FEsV5j/pub?output=csv"

)

df_exercise=pd.read_csv(url_exercise)

# Convertir a enteros en el DataFrame food
columnas_to_clean = ["130 lb", "155 lb", "180 lb", "205 lb"]

for elements in columnas_to_clean:
    df_exercise[elements] = df_exercise[elements].astype(int)

# Mostrar el dataframe
st.write("### Lista de ejercicios por hora:")
st.write(df_exercise)

# Elemento interactivo para que el usuario seleccione alimentos
ejercicio_seleccionado = st.selectbox(
    "Selecciona un ejercicio:",
    df_exercise["Activity, Exercise or Sport (1 hour)"]
)

# Obtener los detalles del alimento seleccionado
detalles_ejercicio = df_exercise[
    df_exercise["Activity, Exercise or Sport (1 hour)"] == ejercicio_seleccionado
]

if not detalles_ejercicio.empty:
    st.write("### Detalles del Ejercicio Seleccionado:")
    st.write(detalles_ejercicio)
else:
    st.write("Selecciona un ejercicio de la lista.")

# Inicializa una variable para realizar,
# el seguimiento del total de calorías quemadas
total_calorias_quemadas = 0

# Variable que almacena varios ejercicios
ejercicios_seleccionados = st.multiselect(
    "Selecciona los ejercicios que has realizado:",
    df_exercise["Activity, Exercise or Sport (1 hour)"]
)

# Obtener los detalles de los ejercicios seleccionados y sumar las calorías
for ejercicio_seleccionado in ejercicios_seleccionados:
    detalles_ejercicio = df_exercise[df_exercise["Activity, Exercise or Sport (1 hour)"] == ejercicio_seleccionado]

    if not detalles_ejercicio.empty and "130 lb" in detalles_ejercicio.columns:
        calorias_ejercicio = detalles_ejercicio["130 lb"].values[0]
        total_calorias_quemadas += calorias_ejercicio
        st.write(f"Detalles del Ejercicio Seleccionado ({ejercicio_seleccionado}):")
        st.write(detalles_ejercicio)
        st.write(f"Calorías quemadas:{calorias_ejercicio}")

# Mostrar el total de calorías quemadas
st.write(f"Total de calorías quemadas: {total_calorias_quemadas}")