# -*- coding: utf-8 -*-
"""datos_iniciales.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w9qkhx_-a0cj01C2fhaSxdYU8bxSAa95
"""

# Importar librerias
import pandas as pd
import streamlit as st
#import streamlit_extras
#import streamlit_authenticator as stauth
#import re
#from deta import Deta
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

# Titulo de la seccion
st.title("Datos iniciales")

# Funcion para cargar las animaciones
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# URL de animacion #1
lottie_mancuerna= load_lottieurl("https://raw.githubusercontent.com/lflunal"
                                 "/ppi_20/main/animaciones/mancuernas.json")

# Mostrar animacion #1
st_lottie(lottie_mancuerna, height = 180, key="mancuerna")

def calcular_horas_de_sueno(hora_sueno, hora_despertar):
    # Obtener las horas de sueño y despertar
    hora_sueno_horas = hora_sueno.hour
    hora_despertar_horas = hora_despertar.hour

    # Calcular la diferencia de horas
    horas_sueno = hora_despertar_horas - hora_sueno_horas

    # Manejar el caso en el que la hora de despertar,
    # sea anterior a la hora de dormir (cruce de medianoche)
    if horas_sueno < 0:
        horas_sueno += 24

    return horas_sueno

# Calcular las calorías necesarias diarias
def calcular_calorias_diarias(sexo, peso, altura, edad, nivel_actividad):
    calorias_diarias = 0  # Inicializar la variable con un valor predeterminado

    if sexo == "Masculino":
        tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
    elif sexo == "Femenino":
        tmb = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)

    if nivel_actividad == "Sedentario":
        calorias_diarias = tmb * 1.2
    elif nivel_actividad == "Ligera actividad":
        calorias_diarias = tmb * 1.375
    elif nivel_actividad == "Moderada actividad":
        calorias_diarias = tmb * 1.55
    elif nivel_actividad == "Alta actividad":
        calorias_diarias = tmb * 1.725
    elif nivel_actividad == "Muy alta actividad":
        calorias_diarias = tmb * 1.9

    return calorias_diarias

# Variable para mostrar diferencia de calorias en base a consumidas - gastadas
def mostrar_diferencia_calorias(total_calorias_consumidas, total_calorias_quemadas, calorias_diarias):
    diferencia_calorias = calorias_diarias - (total_calorias_consumidas - total_calorias_quemadas)
    if diferencia_calorias > 0:
        st.write(f"Has consumido {int(diferencia_calorias)} calorías en exceso hoy. Considera ajustar tu ingesta calórica.")
    elif diferencia_calorias < 0:
        st.write(f"Te faltan {int(abs(diferencia_calorias))} calorías para alcanzar tu ingesta calórica diaria. ¡Asegúrate de comer lo suficiente!")

# Solicitar al usuario ingresar peso y altura
peso = st.number_input("Ingresa tu peso en kilogramos", min_value=0.1)
altura = st.number_input("Ingresa tu altura en centímetros, "
                         "Sin puntos ni comas", step=1)
edad = st.number_input (" Ingrese su edad", step=1)

# Agregar un menú desplegable para seleccionar el sexo
sexo = st.selectbox("Selecciona tu sexo:", ["Masculino", "Femenino"])

# Solicitar al usuario hora de sueño y hora de despertar
hora_sueno = st.time_input("Ingresa la hora en que te dormiste")
hora_despertar = st.time_input("Ingresa la hora en que te despertaste")

# Agregar un menú desplegable para seleccionar el nivel de actividad física
nivel_actividad = st.selectbox("Selecciona tu nivel de actividad física:", [
    "Sedentario",
    "Ligera actividad",
    "Moderada actividad",
    "Alta actividad",
    "Muy alta actividad"
])

# Verificar si el usuario ha ingresado valores válidos
if peso > 0 and altura > 0:
    # Calcular el IMC
    altura_metros = altura / 100
    imc = peso / (altura_metros ** 2)

    # Determinar la categoría de IMC basada en el sexo
    if sexo == "Masculino":
        if isinstance(imc, str):
            st.write(imc)
        else:
            if imc < 18.5:
                categoria = "Bajo peso"
            elif 18.5 <= imc < 24.9:
                categoria = "Peso normal"
            elif 24.9 <= imc < 29.9:
                categoria = "Sobrepeso"
            else:
                categoria = "Obesidad"
            st.write(f"Tu IMC es {imc:.2f}, lo que corresponde a la categoría de "
         f"{categoria} para hombres.")


    elif sexo == "Femenino":
        if isinstance(imc, str):
            st.write(imc)
        else:
            if imc < 18.5:
                categoria = "Bajo peso"
            elif 18.5 <= imc < 24.9:
                categoria = "Peso normal"
            elif 24.9 <= imc < 29.9:
                categoria = "Sobrepeso"
            else:
                categoria = "Obesidad"
            st.write(f"Tu IMC es {imc:.2f}, lo que corresponde a la categoría de "
         f"{categoria} para mujeres.")
else:
    st.write("Por favor, ingresa valores válidos para peso y altura.")

objetivo = st.selectbox("Selecciona tu objetivo:",
                       ["Aumentar masa muscular", "Mantenerse", "Bajar grasa"])

# Mostrar y calcular tiempo de sueño
horas_sueno = calcular_horas_de_sueno(hora_sueno, hora_despertar)

# Mostrar las horas de sueño
st.write(f"Dormiste durante {horas_sueno} horas")

# Llamada a la función y almacenar el resultado
calorias_diarias = calcular_calorias_diarias(sexo, peso, altura, edad, nivel_actividad)

# Mostrar el resultado
st.write(f"Calorías necesarias en un día: {int(calorias_diarias)} calorías")


st.write("### Calculadora de Calorías: ")
# Llamar a la función con los valores adecuados
# Crear un botón para realizar el cálculo
st.button("CALCULAR")

#mostrar_diferencia_calorias(calorias_diarias, total_calorias_quemadas, total_calorias_consumidas)