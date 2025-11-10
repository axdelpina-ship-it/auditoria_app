import streamlit as st
import pandas as pd
import os

EXCEL_FILE = "resultados.xlsx"

# --- Funciones ---
def cargar_datos():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame(columns=["Usuario", "Pregunta1", "Pregunta2", "Pregunta3", "Total"])
    return df

def guardar_respuesta(usuario, respuestas):
    df = cargar_datos()
    total = sum(respuestas)
    nuevo_registro = pd.DataFrame([{
        "Usuario": usuario,
        "Pregunta1": respuestas[0],
        "Pregunta2": respuestas[1],
        "Pregunta3": respuestas[2],
        "Total": total
    }])
    df = pd.concat([df, nuevo_registro], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

# --- App ---
st.title("Encuesta de Satisfacción")

if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Login
if st.session_state.current_user is None:
    usuario_input = st.text_input("Ingresa tu usuario:")
    if st.button("Ingresar"):
        if usuario_input:
            st.session_state.current_user = usuario_input
            st.success(f"Bienvenido, {usuario_input}")
else:
    st.write(f"Usuario: {st.session_state.current_user}")

    if not st.session_state.submitted:
        # Encuesta
        st.subheader("Responde la encuesta:")
        q1 = st.slider("Pregunta 1: ¿Qué tan satisfecho estás con el servicio?", 1, 5, 3)
        q2 = st.slider("Pregunta 2: ¿Recomendarías nuestro servicio?", 1, 5, 3)
        q3 = st.slider("Pregunta 3: ¿Qué tan fácil fue usar nuestra plataforma?", 1, 5, 3)

        if st.button("Enviar respuestas"):
            respuestas = [q1, q2, q3]
            guardar_respuesta(st.session_state.current_user, respuestas)
            st.session_state.submitted = True
            st.success("¡Respuestas guardadas correctamente!")

    else:
        st.info("Gracias por enviar tus respuestas.")
        if st.button("Cerrar sesión"):
            st.session_state.current_user = None
            st.session_state.submitted = False

    # Ver resultados (opcional)
    if st.checkbox("Ver todos los resultados"):
        df = cargar_datos()
        st.dataframe(df)
