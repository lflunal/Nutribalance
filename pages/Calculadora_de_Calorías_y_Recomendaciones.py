
# Importar librerias
import pandas as pd
import streamlit as st
#import streamlit_extras
from streamlit_lottie import st_lottie
import requests
import re
import streamlit_authenticator as stauth
from deta import Deta
from datetime import datetime
import matplotlib.pyplot as plt

# Almacenamos la key de la base de datos en una constante
DETA_KEY = "e0qgr2zg4tq_mbZWcCg7iGCpWFBbCy3GGFjEYHdFmZYR"

# Creamos nuestro objeto deta para hacer la conexion a la DB
deta = Deta(DETA_KEY)

# Realizamos la conexion a la DB
db = deta.Base("NutribalanceUsers")

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

# Funcion que retorna la altura de un usuario
def get_user_height(sel_user):
    """
    Regresa la altura de un usuario seleccionado
    Parametro sel_user: El usuario del que se desea obtener la altura
    """

    users = db.fetch()
    height = 0
    for user in users.items:
        if user["username"] == sel_user:
            height = user["height"]
            return int(height)

# Funcion que retorna la edad de un usuario
def get_user_age(sel_user):
    """
    Regresa la edad de un usuario seleccionado
    Parametro sel_user: El usuario del que se desea obtener la altura
    """

    users = db.fetch()
    current_date = datetime.today()

    for user in users.items:
        if user["username"] == sel_user:
            dob_str = user["age"]
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            age = (current_date.date() - dob).days // 365
            return age

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
    """Retorna True si el email ingresado es valido,
    de lo contrario retorna False"""
    # Patrones tipicos de un email valido
    pattern = "^[a-zA-Z0_9-_]+@[a-zA-Z0_9-_]+\.[a-z]{1,3}$"
    pattern1 = "^[a-zA-Z0_9-_]+@[a-zA-Z0_9-_]+\.[a-z]{1,3}+\.[a-z]{1,3}$"

    # Verifica si el email ingresado coincide con algun patron definido
    if re.match(pattern, email) or re.match(pattern1, email):
        return True
    return False

# Funcion que verifica si un username ingresado es valido
def validar_username(username):
    """Retorna True si el username es valido, de lo contrario,
    retorna False"""
    # Se define el patron de un username tipico
    pattern = "^[a-zA-Z0-9]*$"
    # Se verifica si el username ingresado coincide con el patron tipico
    if re.match(pattern, username):
        return True
    return False

def get_datos_nutricionales(email):
    usuario = db.get(email)
    return usuario.get("food", [])

# Manejo de posibles errores
try:
    # Se almacenan los datos necesarios de la DB
    users = fetch_usuarios()
    emails = get_emails_usuarios()
    usernames = get_usernames_usuarios()
    passwords = [user["password"] for user in users]

    # Se crea el diccionario credentials necesario para
    # el funcionamiento del autenticador de cuentas
    credentials = {"usernames" : {}}
    for index in range(len(emails)):
        credentials["usernames"][usernames[index]] = {"name" : emails[index],
                                                "password" : passwords[index]}

    # Creacion del autenticador
    Authenticator = stauth.Authenticate(credentials, cookie_name="Streamlit",
                                        key="cookiekey", cookie_expiry_days=3)

    # Crear boton de Cerrar sesion si la sesion fue iniciada
    if st.session_state["authentication_status"]:
        email, authentication_status, username = Authenticator.login(\
    "Ingresar", "main"
)

        Authenticator.logout("Cerrar sesion", location="sidebar")

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
  "https://docs.google.com/spreadsheets/d/e/2PACX"
  "-1vTRvtsx_JsvwK7xeQ-tB-Q6zOsAv3hmo5t4On_FQicArs50"
  "-N0QJy60J3DH6rNsxRJgHLlGXCinT9yO/pub?output=csv"
  )


# Cargar el DataFrame desde la URL y ordenar alfabeticamente
df_foods_base = pd.read_csv(url_foods)
df_foods_base = df_foods_base.sort_values("Food")

# Eliminar comas y convertir a enteros en el DataFrame food
columns_to_clean = ["Calories", "Grams", "Protein", "Fat","Sat.Fat",
                    "Fiber", "Carbs"]

for column in columns_to_clean:
    df_foods_base[column] = df_foods_base[column].str.replace(',',
                                                              '', regex=True)
    df_foods_base[column] = df_foods_base[column].str.replace('t',
                                                              '0', regex=True)
    df_foods_base[column] = df_foods_base[column].str.replace('a',
                                                              '0', regex=True)
    df_foods_base[column] = df_foods_base[column].str.replace("'",
                                                              '', regex=True)
    df_foods_base[column] = df_foods_base[column].str.strip()
    df_foods_base[column] = df_foods_base[column].str.replace(',',
                                                              '.', regex=True)
    df_foods_base[column] = df_foods_base[column].replace('', '0')
    df_foods_base[column] = df_foods_base[column].astype(float) \
    .fillna(0).astype(int)

# Funcion proteinas diarias
def calcular_proteinas_diarias(peso, objetivo):
    if objetivo == "Aumentar masa muscular":
        proteinas_diarias = peso * 2.2
        return proteinas_diarias
    elif objetivo == "Mantenerse en un peso":
        proteinas_diarias = peso * 1.5
        return proteinas_diarias
    elif objetivo == "Bajar de peso":
        proteinas_diarias = peso * 1.2
        return proteinas_diarias

# Funcion grasas diarias
def calcular_grasas_diarias(peso, objetivo):
    if objetivo == "Aumentar masa muscular":
        grasas_diarias = peso * 1
        return grasas_diarias
    elif objetivo == "Mantenerse en un peso":
        grasas_diarias = peso * 0.8
        return grasas_diarias
    elif objetivo == "Bajar de peso":
        grasas_diarias = peso * 0.6
        return grasas_diarias

# Funcion carbohidratos diarios
def calcular_carbohidratos_diarios(calorias_diarias, proteinas, grasas):
    carbohidratos_diarios = (calorias_diarias - (proteinas * 4 + grasas * 9)) / 4
    return carbohidratos_diarios

# Funcion para mostrar recomendaciones de carbohidratos segun los alimentos seleccionados
def mostrar_diferencia_carbohidratos(total_carbohidratos_consumidos, carbohidratos_diarios):
   diferencia_carbohidratos = carbohidratos_diarios - total_carbohidratos_consumidos
   if diferencia_carbohidratos > 0:
        st.write(f"Has consumido {int(diferencia_carbohidratos)} gramos de carbohidratos en exceso hoy. Considera ajustar tu ingesta.")
   elif diferencia_carbohidratos < 0:
        st.write(f"Te faltan {int(abs(diferencia_carbohidratos))} gramos de carbohidratos para alcanzar tu ingesta diaria. ¡Asegúrate de consumir suficientes carbohidratos!")
        st.write(f"**Te recomendamos que consumas los siguientes alimentos con más carbohidratos**")
        top_carbs = df_foods_base.nlargest(5, 'Carbs')
        st.write(top_carbs)
   else:
        st.write("Estás en línea con tu ingesta diaria de carbohidratos. ¡Bien hecho!")

# Funcion para mostrar recomendaciones de grasas segun los alimentos seleccionados
def mostrar_diferencia_grasas(total_grasas_consumidas, grasas_diarias):
    diferencia_grasas = grasas_diarias - total_grasas_consumidas

    if diferencia_grasas > 0:
        st.write(f"Has consumido {int(diferencia_grasas)} gramos de grasas en exceso hoy. Considera ajustar tu ingesta.")
    elif diferencia_grasas < 0:
        st.write(f"Te faltan {int(abs(diferencia_grasas))} gramos de grasas para alcanzar tu ingesta diaria. ¡Asegúrate de consumir suficientes grasas!")
    else:
        st.write("Estás en línea con tu ingesta diaria de grasas. ¡Bien hecho!")

# Funcion para mostrar recomendaciones de proteinas segun los alimentos seleccionados
def mostrar_diferencia_proteinas(total_proteinas_consumidas, proteinas_diarias):
    diferencia_proteinas = proteinas_diarias - total_proteinas_consumidas

    if diferencia_proteinas > 0:
        st.write(f"Has consumido {int(diferencia_proteinas)} gramos de proteínas en exceso hoy. Considera ajustar tu ingesta.")
    elif diferencia_proteinas < 0:
        st.write(f"Te faltan {int(abs(diferencia_proteinas))} gramos de proteínas para alcanzar tu ingesta diaria. ¡Asegúrate de consumir suficientes proteínas!")
        st.write(f"**Te recomendamos que consumas los siguientes alimentos con más proteínas**")
        top_protein = df_foods_base.nlargest(5, 'Protein')
        st.write(top_protein)
    else:
        st.write("Estás en línea con tu ingesta diaria de proteínas. ¡Bien hecho!")


# Titulo de la seccion
st.title("Calculadora de Calorias y Recomendaciones")

# Funcion para cargar las animaciones
def load_lottieurl(url):
    """
    Carga un archivo JSON Lottie desde una URL.

    Parameters:
    - url (str): La URL desde la cual cargar el archivo JSON Lottie.

    Returns:
    - dict or None: Un diccionario que representa el contenido del archivo
    JSON Lottie si la carga es exitosa, o None si hay un error al acceder
    a la URL o el código de estado no es 200 (OK).
    """
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
    """
   Calcula la cantidad de horas de sueño entre la hora de dormir
   y la hora de despertar.

   Parameters:
   - hora_sueno (datetime): Objeto datetime que representa la hora de dormir.
   - hora_despertar (datetime): Objeto datetime que representa
   la hora de despertar.

   Returns:
   - int: La cantidad de horas de sueño calculadas.
   """
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
    """
   Calcula el número estimado de calorías diarias necesarias
   según varios factores.

   Parameters:
   - sexo (str): Género del individuo ("Masculino" o "Femenino").
   - peso (float): Peso en kilogramos.
   - altura (float): Altura en centímetros.
   - edad (int): Edad en años.
   - nivel_actividad (str): Nivel de actividad física del individuo.

   Returns:
   - float: Número estimado de calorías diarias necesarias
   según los factores dados.
   """
   # Inicializar la variable con un valor predeterminado
    calorias_diarias = 0

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
def mostrar_diferencia_calorias(total_calorias_consumidas,
                                calorias_diarias):
    """
    Muestra un mensaje indicando la diferencia entre las calorías consumidas
    y quemadas respecto a la ingesta calórica diaria recomendada.

    Parameters:
    - total_calorias_consumidas (float): Total de calorías consumidas
    durante el día.
    - total_calorias_quemadas (float): Total de calorías quemadas
    durante el día.
    - calorias_diarias (float): Ingesta calórica diaria recomendada.

    Returns:
    - None: No hay un valor de retorno específico;
    la función imprime un mensaje según la diferencia de calorías.
    """
    diferencia_calorias = (calorias_diarias - total_calorias_consumidas)

    if diferencia_calorias > 0:
        st.write(f"Has consumido {int(diferencia_calorias)} calorías en"
                 "excesohoy. Considera ajustar tu ingesta calórica.")
    elif diferencia_calorias < 0:
        st.write(f"Te faltan {int(abs(diferencia_calorias))} calorías para "
                 "alcanzar tu ingesta calórica diaria. ¡Asegúrate de comer"
                 "lo suficiente!")

# Solo generar el formulario de ingreso de datos si el usuario inicia sesion
if st.session_state["authentication_status"]:
    # Solicitar al usuario ingresar peso
    peso = st.number_input("Ingresa tu peso en kilogramos", min_value=0.1)

    # Solicitar al usuario ingresar peso
    height = st.number_input("Ingresa tu altura en cm sin puntos ni comas")
    altura = int(height)

    # Recolectar los datos de un usuario que haya ingresado
    #if st.session_state["authentication_status"]:
    #    altura = get_user_height(username)
    #else:
     #   altura = 0
    if st.session_state["authentication_status"]:
        edad = get_user_age(username)
    else:
        edad = 0

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

    objetivo = st.selectbox("Selecciona tu objetivo:",
                        ["Aumentar masa muscular", "Mantenerse en un peso",
                            "Bajar de peso"])

    # Mostrar y calcular tiempo de sueño
    horas_sueno = calcular_horas_de_sueno(hora_sueno, hora_despertar)

    # Mostrar las horas de sueño
    st.write(f"Dormiste durante {horas_sueno} horas")

    st.write("### Calculadora de Calorías: ")
    # Llamar a la función con los valores adecuados
    # Crear un botón para realizar el cálculo
    boton_calcular = st.button("CALCULAR")

    # Verifica si el usuario presiona el boton
    if boton_calcular:
        st.write("### RECOMENDACIONES")

        # Verifica si el usuario inicio sesion
        if st.session_state["authentication_status"]:

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
                        st.write(f"Tu IMC es {imc:.2f}, lo que corresponde"
                                "a la categoría de "
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
                        st.write(f"Tu IMC es {imc:.2f}, lo que corresponde"
                                "a la categoría de "
                                f"{categoria} para mujeres.")
            else:
                st.write("Por favor, ingresa valores válidos para peso y altura.")
            calorias_diarias = calcular_calorias_diarias(sexo, peso, altura,
                                                        edad, nivel_actividad)

            # Mostrar el resultado
            st.write(f"Calorías necesarias en un día: "
                    f"{int(calorias_diarias)} calorías")
            datos_usuario = get_datos_nutricionales(email)

            # Convierte los datos a un formato que se puede utilizar fácilmente
            datos = []
            for comida in datos_usuario:
                try:
                    fecha = datetime.strptime(comida[0], "%Y-%m-%d")
                except (ValueError, TypeError):
                    # Fecha predeterminada si hay un problema con el formato
                    fecha = datetime.now()

                calorias = comida[1] if len(comida) > 1 else 0
                carbohidratos = comida[2] if len(comida) > 2 else 0
                grasa = comida[3] if len(comida) > 3 else 0
                fibra = comida[4] if len(comida) > 4 else 0
                proteinas = comida[5] if len(comida) > 5 else 0
                datos.append([fecha, calorias, carbohidratos, grasa,
                            fibra, proteinas])

            # Crea un DataFrame de pandas
            columnas = ["Fecha", "Calorias", "Carbohidratos", "Grasa",
                        "Fibra", "Proteinas"]
            df = pd.DataFrame(datos, columns=columnas)

            # Calcular calorías semanales
            # Obtener el nombre del día de la semana
            df["DiaSemana"] = pd.to_datetime(df["Fecha"]).dt.strftime('%A')

            # Obtener la fecha de hace 7 días a partir de
            # la fecha más reciente en los datos
            fecha_limite = df["Fecha"].max() - pd.DateOffset(days=6)

            # Filtrar los últimos 7 días
            df_ultimos_7_dias = df[df['Fecha'] >= (datetime.now() - pd.DateOffset(days=7))]

            # Mostrar recomendaciones
            # mostrar_diferencia_calorias(df_ultimos_7_dias["Calorias"].sum(),calcular_calorias_diarias,total_calorias_quemadas)
            mostrar_diferencia_carbohidratos(df_ultimos_7_dias["Carbohidratos"].sum(),
                                            calcular_carbohidratos_diarios(calorias_diarias, df_ultimos_7_dias["Proteinas"].sum(),
                                                                            df_ultimos_7_dias["Grasa"].sum()))
            mostrar_diferencia_proteinas(df_ultimos_7_dias["Proteinas"].sum(),
                                        calcular_proteinas_diarias(peso, objetivo))
            mostrar_diferencia_grasas(df_ultimos_7_dias["Grasa"].sum(),
                                        calcular_grasas_diarias(peso, objetivo))

else:
    st.warning("Si desea calcular sus resultados debe [iniciar sesion]"
                "(https://5appmb9yhjafnikthscthm.streamlit.app/Ingresar)"
                " O [registrarse]"
                "(https://5appmb9yhjafnikthscthm.streamlit.app/Registrarse)")
