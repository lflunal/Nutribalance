# -*- coding: utf-8 -*-
"""Registro_Alimentos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t2nWYYDxc12UcbpLPDiA1FnXazMF5wh1
"""

# Importar librerias
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
import requests

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


# Lectura de datos
url_foods = (
  "https://docs.google.com/spreadsheets/d/e/2PACX-1vRHczI8B0Qbww2boToqMi"
  "G-wi7T3N5fq9QcEFqryMGuWi0yFT7ty1vZTXgeAgf4S9HyDqy8APfmdWtQ/pub?output=csv"
  )


# Cargar el DataFrame desde la URL
df_foods_base = pd.read_csv(url_foods)

# Eliminar comas y convertir a enteros en el DataFrame food
columns_to_clean = ["Calories", "Grams", "Protein", "Fat","Sat.Fat",
                    "Fiber", "Carbs"]

for column in columns_to_clean:
    df_foods_base[column] = df_foods_base[column].str.replace(',', '', regex=True)
    df_foods_base[column] = df_foods_base[column].str.replace('t', '0', regex=True)
    df_foods_base[column] = df_foods_base[column].str.replace('a', '0', regex=True)
    df_foods_base[column] = df_foods_base[column].str.replace("'", '', regex=True)
    df_foods_base[column] = df_foods_base[column].str.strip()
    df_foods_base[column] = df_foods_base[column].str.replace(',', '.', regex=True)
    df_foods_base[column] = df_foods_base[column].replace('', '0')
    df_foods_base[column] = df_foods_base[column].astype(float).fillna(0).astype(int)


# Configuración de la aplicación Streamlit
st.title("Registro de Alimentos Consumidos en el Día")

# Seleccionar posibles alergias o disgustos de algun alimento
alergias_seleccionadas = st.multiselect(
    "Selecciona los alimentos que no desea incluir:",
    df_foods_base["Food"]
)

# Inicializa una variable para realizar el seguimiento del total de calorías
total_calorias_consumidas = 0
total_carbohidratos_consumidas = 0
total_proteinas_consumidas = 0
total_grasa_saturada_consumidas = 0
total_fibra_consumida_consumidas = 0

# Guardamos inicialmente todos los alimentos en df_foods
df_foods = df_foods_base

# Ocultar del dataframe los elementos seleccionados
for alergia in alergias_seleccionadas:
    df_foods = df_foods[df_foods["Food"] != alergia]

st.write("### Lista de Alimentos:")
st.write(df_foods)

# Variable para la selecion de varias comidas
alimentos_seleccionados = st.multiselect(
    "Selecciona los alimentos que has consumido:",
    df_foods["Food"]
)

# Obtener los detalles de los alimentos seleccionados
for alimento_seleccionado in alimentos_seleccionados:
    detalles_alimento = df_foods[df_foods["Food"] == alimento_seleccionado]
    if not detalles_alimento.empty:
        st.write(f"### Detalles del Alimento Seleccionado ({alimento_seleccionado}):")
        calorias_alimento = detalles_alimento["Calories"].values[0]
        total_calorias_consumidas += calorias_alimento
        carbohidratos_alimento = detalles_alimento["Carbs"].values[0]
        total_carbohidratos_consumidas += carbohidratos_alimento
        proteina_alimento = detalles_alimento["Protein"].values[0]
        total_proteinas_consumidas += proteina_alimento
        grasas_saturadas_alimento = detalles_alimento["Sat.Fat"].values[0]
        total_grasa_saturada_consumidas += grasas_saturadas_alimento
        fibra_alimento = detalles_alimento["Fiber"].values[0]
        total_fibra_consumida_consumidas += fibra_alimento
        st.write(detalles_alimento)

    else:
        st.write(f"Selecciona un alimento de la lista o verifica la ortografía.")

# Mostrar el total de valorico consumido (calorias, carb, grasas...)
st.write(f"Total de calorías consumidas: {total_calorias_consumidas} calorías")
st.write(f"Total de carbohidratos consumidos: {total_carbohidratos_consumidas} ")
st.write(f"Total de grasas saturadas consumida: {total_grasa_saturada_consumidas} ")
st.write(f"Total de fibra consumida: {total_fibra_consumida_consumidas} ")
st.write(f"Total de proteina consumida: {total_proteinas_consumidas} ")

# Funcion para cargar las animaciones
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# URL de animacion #1
lottie_peso = load_lottieurl("https://raw.githubusercontent.com/lflunal/"
"ppi_20/main/animaciones/peso.json")

# Mostrar animacion #1
st_lottie(lottie_peso, height = 180, key="peso")