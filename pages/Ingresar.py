import yaml
from yaml.loader import SafeLoader
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page

file_path = Path(__file__).parent / "usuariosTest.yaml"
with file_path.open() as file:
    datos_usuarios = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    datos_usuarios["credentials"],
    datos_usuarios["cookie"]["name"],
    datos_usuarios["cookie"]["key"],
    datos_usuarios["cookie"]["expiry_days"]
)


authenticator.login("Ingresar", "main")


if st.session_state["authentication_status"]:
    authenticator.logout("Cerrar sesion", "sidebar", key="unique_key")
    switch_page("Nutribalance")

elif st.session_state["authentication_status"] is False:
    st.error("Usuario o contraseña incorrecto(s)")

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