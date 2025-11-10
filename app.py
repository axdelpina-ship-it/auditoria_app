import streamlit as st
import pandas as pd
import os

# Nombre del archivo Excel donde se guardarán los resultados
EXCEL_FILE = "resultados.xlsx"

# --- Funciones ---
def cargar_datos():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        # Crear DataFrame vacío si no existe el archivo
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

# --- Streamlit App ---
st.title("Encuesta de Satisfacción")

# Login simple
if "current_user" not in st.session_state:
    st.session_state.current_user = None

if st.session_state.current_user is None:
    usuario_input = st.text_input("Ingresa tu usuario:")
    if st.button("Ingresar"):
        if usuario_input:
            st.session_state.current_user = usuario_input
            st.success(f"Bienvenido, {usuario_input}")
            st.experimental_rerun()
else:
    st.write(f"Usuario: {st.session_state.current_user}")

    # Preguntas
    st.subheader("Responde la encuesta:")
    q1 = st.slider("Pregunta 1: ¿Qué tan satisfecho estás con el servicio?", 1, 5, 3)
    q2 = st.slider("Pregunta 2: ¿Recomendarías nuestro servicio?", 1, 5, 3)
    q3 = st.slider("Pregunta 3: ¿Qué tan fácil fue usar nuestra plataforma?", 1, 5, 3)

    if st.button("Enviar respuestas"):
        respuestas = [q1, q2, q3]
        guardar_respuesta(st.session_state.current_user, respuestas)
        st.success("¡Respuestas guardadas correctamente!")
        # Limpiar sesión para que el usuario pueda cerrar sesión si quiere
        st.session_state.current_user = None
        st.experimental_rerun()

    # Mostrar resultados (opcional, solo para testing)
    if st.checkbox("Ver todos los resultados"):
        df = cargar_datos()
        st.dataframe(df)
