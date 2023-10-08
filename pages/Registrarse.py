import yaml
from yaml.loader import SafeLoader
from pathlib import Path

import streamlit as st
import streamlit_extras
import streamlit_authenticator as stauth

file_path = Path(__file__).parent / "usuariosTest.yaml"
with file_path.open() as file:
    datos_usuarios = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    datos_usuarios["credentials"],
    datos_usuarios["cookie"]["name"],
    datos_usuarios["cookie"]["key"],
    datos_usuarios["cookie"]["expiry_days"]
)

if st.session_state["authentication_status"]:
    authenticator.logout("Cerrar sesion", "sidebar", key="unique_key")

try:
    if authenticator.register_user("Registrar Usuario", preauthorization=False):
        with open(file_path, "w") as file:
            yaml.dump(datos_usuarios, file, default_flow_style=False)
        st.success("Usuario registrado")
except Exception as e:
    st.error(e)

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