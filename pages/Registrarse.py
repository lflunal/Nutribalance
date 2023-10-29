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
    return db.put({"key":email, "username": username, "age":age, "height":height, "password":password, "food":[]})

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

# Formulario de registro con los datos que debe ingresar el usuario
def registro():
    """Formulario de registro que guarda un registro de usuario en la DB si este es valido"""

    # Se define un checkbox en el que se deben aceptar los T&C antes de enviar un registro
    st.write("Debe aceptar los terminos y condiciones antes de poder enviar el formulario")
    aceptar_terminos = st.checkbox("Acepto los [Términos y Condiciones](https://github.com/\
lflunal/ppi_20/blob/Luis-Lopez/Politica%20de%20Tratamiento%20de%20Datos.md)")

    # Creacion del formulario
    with st.form(key="registro", clear_on_submit=True):
        # Titulo del formulario
        st.subheader("Registrarse")

        # Campos a ser llenados por el usuario
        email = st.text_input("Email", placeholder="Ingrese su Email")
        username = st.text_input("Usuario", placeholder="Ingrese su nombre de usuario")
        age = st.text_input("Edad (en años)", placeholder="Ingrese su edad en años")
        height = st.text_input("Altura (en cm sin puntos ni comas)", placeholder="Ingrese su estatura en cm sin puntos ni comas")
        password = st.text_input("Contraseña", placeholder="Ingrese su contraseña", type="password")

            # Si se aceptan los términos y condiciones, habilitar el botón de envío
        if aceptar_terminos:
            # Boton de envio de datos de registro
            st.form_submit_button("Registrate")
        else:
            st.warning("Debes aceptar los términos y condiciones antes de enviar el formulario")

        # Revisar validez de los datos ingresados por el usuario y registro a la DB
        if email and username and age and height and password:
            if validar_email(email):
                if email not in get_emails_usuarios():
                    if validar_username(username):
                        if username not in get_usernames_usuarios():
                            password_encriptada = stauth.Hasher([password]).generate()
                            insertar_usuario(email, username, age, height, password_encriptada[0])
                            st.success("Cuenta creada con exito!")
                        else:
                            st.warning("Nombre de usuario en uso")
                    else:
                        st.warning("Nombre de usuario invalido (solo debe tener letras y numeros)")
                else:
                    st.warning("El email ya esta en uso")
            else:
                st.warning("Email invalido")
        else:
            st.warning("Debe rellenar todos los campos")

# Manejo de posibles errores
try:
    # Se almacenan los datos necesarios de la DB
    users = fetch_usuarios()
    emails = get_emails_usuarios()
    usernames = get_usernames_usuarios()
    passwords = [user["password"] for user in users]

    # Se crea el diccionario credentials necesario para el funcionamiento del autenticador de cuentas
    credentials = {"usernames" : {}}
    for index in range(len(emails)):
        credentials["usernames"][usernames[index]] = {"name" : emails[index], "password" : passwords[index]}

    # Creacion del autenticador
    Authenticator = stauth.Authenticate(credentials, cookie_name="Streamlit", key="cookiekey", cookie_expiry_days=3)

    # Crear boton de Cerrar sesion si la sesion fue iniciada
    if st.session_state["authentication_status"]:
        Authenticator.logout("Cerrar sesion", location="sidebar")
        st.write("Ya ha iniciado sesion")

    # Si la sesion no fue iniciada, ejecutar el formulario de registro
    else:
        registro()

# Informar de que hubo una excepcion en caso de que la haya
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
#st.markdown(footer,unsafe_allow_html=True)