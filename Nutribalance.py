#%%writefile app.py
import pandas as pd

import yaml
from yaml.loader import SafeLoader
from pathlib import Path

import streamlit as st
import streamlit_extras
import streamlit_authenticator as stauth

file_path = Path(__file__).parent / "pages/usuariosTest.yaml"
with file_path.open() as file:
    datos_usuarios = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    datos_usuarios["credentials"],
    datos_usuarios["cookie"]["name"],
    datos_usuarios["cookie"]["key"],
    datos_usuarios["cookie"]["expiry_days"]
)

st.title("Nutribalance")

if st.session_state["authentication_status"]:
    authenticator.logout("Cerrar sesion", "sidebar", key="unique_key")

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

# Función para calcular el IMC
st.title("Calculadora de IMC")
def calcular_imc(peso, altura):
    try:
      # Convertir la altura de cm a metros
        altura_metros = altura / 100
        imc = peso / (altura_metros ** 2)
        return imc
    except ZeroDivisionError:
        return "La altura no puede ser cero."

# Calcular las calorias diarias:
# Falta imprimirlo y nivel de actividad
def calcular_calorias_diarias(sexo, peso, altura, edad, nivel_actividad):
    if sexo == "Masculino":
        tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
    elif sexo == "Femenino":
        tmb = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)

    if nivel_actividad == "sedentario":
        calorias_diarias = tmb * 1.2
    elif nivel_actividad == "ligera_actividad":
        calorias_diarias = tmb * 1.375
    elif nivel_actividad == "moderada_actividad":
        calorias_diarias = tmb * 1.55
    elif nivel_actividad == "alta_actividad":
        calorias_diarias = tmb * 1.725
    elif nivel_actividad == "muy_alta_actividad":
        calorias_diarias = tmb * 1.9


# Función para determinar la categoría de IMC
def determinar_categoria(imc):
    if imc < 18.5:
        return "Bajo peso"
    elif 18.5 <= imc < 24.9:
        return "Peso normal"
    elif 24.9 <= imc < 29.9:
        return "Sobrepeso"
    else:
        return "Obesidad"

# Solicitar al usuario ingresar peso y altura
peso = st.number_input("Ingresa tu peso en kilogramos", min_value=0.1)
altura = st.number_input("Ingresa tu altura en centímetros, "
                         "Sin puntos ni comas", step=1)
edad = st.number_input (" Ingrese su edad", step=1)

# Agregar un menú desplegable para seleccionar el sexo
sexo = st.selectbox("Selecciona tu sexo:", ["Masculino", "Femenino"])

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
                       ["Aumentar", "Mantenerse", "Bajar"])



#lectura de datos
url_foods = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSOahgzh7JD0eqEEOE5DdXPqJci2D7ZH16nb8Ski1OcZkR448sOMPRE"
    "LuLLEG4EiNuNhWz5DpaAHf8E/pub?output=csv"
)

url_exercise = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTXXom0c0qWSJIPrIQZo_0qGxSzoM0u_xe8Cijv1ZAY"
    "bP6EKshVAtvwVV2eh5Yj1Ueio8tzb7FEsV5j/pub?output=csv"
)

# Cargar el DataFrame desde la URL
df_foods = pd.read_csv(url_foods)
df_exercise=pd.read_csv(url_exercise)

# Configuración de la aplicación Streamlit
st.title("Registro de Alimentos Consumidos en el Día")

# Mostrar el DataFrame en la página web
st.write("### Lista de Alimentos:")
st.write(df_foods)

# Elemento interactivo para que el usuario seleccione alimentos
alimento_seleccionado = st.selectbox(
    "Selecciona un alimento:", df_foods["Food"]
)

# Obtener los detalles del alimento seleccionado
detalles_alimento = df_foods[df_foods["Food"] == alimento_seleccionado]

if not detalles_alimento.empty:
    st.write("### Detalles del Alimento Seleccionado:")
    st.write(detalles_alimento)
else:
    st.write("Selecciona un alimento de la lista.")

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