# Pagina de inicio de sesion

# Importar librerias necesarias
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

try:
    users = fetch_usuarios()
    emails = get_emails_usuarios()
    usernames = get_usernames_usuarios()
    passwords = [user["password"] for user in users]

    credentials = {"usernames" : {}}
    for index in range(len(emails)):
        credentials["usernames"][usernames[index]] = {"name" : emails[index], "password" : passwords[index]}
    
    Authenticator = stauth.Authenticate(credentials, cookie_name="Streamlit", key="cookiekey", cookie_expiry_days=3)

    email, authentication_status, username = Authenticator.login("Ingresar", "main")

    if username:
        if username in usernames:
            if authentication_status:
                st.write(f"Bienvenido {username}")
                Authenticator.logout("Cerrar sesion", location="sidebar")
            elif not authentication_status:
                st.warning("Contraseña o nombre de usuario incorrectos")
            else:
                st.warning("Por favor ingrese todos los campos")
        else:
            st.warning("Nombre de usuario no existe, por favor registrese")


except:
    st.error("Excepcion lanzada")

# Crear pie de pagina con los datos de contacto de los creadores
footer = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
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