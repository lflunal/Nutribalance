#%%writefile app.py
# Pagina prinipal de la app Nutribalance

# Importar librerias
import pandas as pd
import streamlit as st
import streamlit_extras
import streamlit_authenticator as stauth
import re
from deta import Deta


# Almacenamos la key de la base de datos en una constante
DETA_KEY = "e0qgr2zg4tq_mbZWcCg7iGCpWFBbCy3GGFjEYHdFmZYR"

# Creamos nuestro objeto deta para hacer la conexion a la DB
deta = Deta(DETA_KEY)

# Realizamos la conexion a la DB
db = deta.Base("NutribalanceUsers")

# Funcion para registrar usuarios en la DB
def insertar_usuario(email, username, age, height, password):
    """Agrega usuarios a la Base de Datos"""
    return db.put({"key":email, "username": username, "age":age, "height":height, "password":password})

# Funcion que retorna los usuarios registrados
def fetch_usuarios():
    """Regresa un diccionario con los usuarios registrados"""
    # guardamos los datos de la DB en users y retornamos su contenido
    users = db.fetch()
    return users.items

# Funcion que retorna los emails de los usuarios registrados
def get_emails_usuarios():
    """Regresa una lista con los emails de cada usuario"""
    # guardamos los datos de la DB en users
    users = db.fetch()
    emails = []
    # filtramos los emails de la DB
    for user in users.items:
        emails.append(user["key"])
    return emails

# Funcion que retorna los nombres de usuario de los usuarios registrados
def get_usernames_usuarios():
    """Regresa una lista con los username de cada usuario"""
    # guardamos los datos de la DB en users
    users = db.fetch()
    usernames = []
    # filtramos los usernames de la DB
    for user in users.items:
        usernames.append(user["username"])
    return usernames

# Funcion que verifica si un email ingresado es valido
def validar_email(email):
    """Retorna True si el email ingresado es valido, de lo contrario retorna False"""
    # Patrones tipicos de un email valido
    pattern = "^[a-zA-Z0_9-_]+@[a-zA-Z0_9-_]+\.[a-z]{1,3}$"
    pattern1 = "^[a-zA-Z0_9-_]+@[a-zA-Z0_9-_]+\.[a-z]{1,3}+\.[a-z]{1,3}$"

    # Verifica si el email ingresado coincide con algun patron definido
    if re.match(pattern, email) or re.match(pattern1, email):
        return True
    return False

# Funcion que verifica si un username ingresado es valido
def validar_username(username):
    """Retorna True si el username es valido, de lo contrario, retorna False"""
    # Se define el patron de un username tipico
    pattern = "^[a-zA-Z0-9]*$"
    # Se verifica si el username ingresado coincide con el patron tipico
    if re.match(pattern, username):
        return True
    return False

# Obtener el camino hacia el archivo usuariosTest.yaml donde se guardan los usuari
# Titulo en la pagina
st.title("Nutribalance")

try:
    users = fetch_usuarios()
    emails = get_emails_usuarios()
    usernames = get_usernames_usuarios()
    passwords = [user["password"] for user in users]

    credentials = {"usernames" : {}}
    for index in range(len(emails)):
        credentials["usernames"][usernames[index]] = {"name" : emails[index], "password" : passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name="Streamlit", key="cookiekey", cookie_expiry_days=3)

    if st.session_state["authentication_status"]:
        Authenticator.logout("Cerrar sesion", location="sidebar")

except:
    st.error("Excepcion lanzada")

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