import streamlit as st
import pandas as pd
import os

# ---- ARCHIVO EXCEL ----
EXCEL_FILE = "data.xlsx"

# Crear Excel vacío si no existe
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Usuario", "Pregunta1", "Pregunta2", "Pregunta3", "Total"])
    df.to_excel(EXCEL_FILE, index=False)

# ---- FUNCIONES ----
def cargar_datos():
    return pd.read_excel(EXCEL_FILE)

def guardar_respuesta(usuario, respuestas):
    df = cargar_datos()
    total = sum(respuestas)
    df = df.append({"Usuario": usuario,
                    "Pregunta1": respuestas[0],
                    "Pregunta2": respuestas[1],
                    "Pregunta3": respuestas[2],
                    "Total": total}, ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

def mostrar_ranking():
    df = cargar_datos()
    df_sorted = df.sort_values(by="Total", ascending=False)
    st.subheader("🏆 Ranking de usuarios")
    st.dataframe(df_sorted)

# ---- LOGIN / REGISTRO ----
st.title("🎮 Carrera de Satisfacción")

# Lista de usuarios
if "usuarios" not in st.session_state:
    st.session_state.usuarios = []

usuario = st.text_input("Ingresa tu nombre de usuario")

if st.button("Entrar"):
    if usuario:
        st.session_state.current_user = usuario
        st.success(f"Bienvenido {usuario}")
    else:
        st.error("Ingresa un nombre válido")

# ---- ENCUESTA ----
if "current_user" in st.session_state:
    st.subheader("Responde la encuesta")
    pregunta1 = st.slider("Pregunta 1: ¿Qué tan satisfecho estás?", 0, 10, 5)
    pregunta2 = st.slider("Pregunta 2: ¿Cómo calificarías la atención?", 0, 10, 5)
    pregunta3 = st.slider("Pregunta 3: ¿Volverías a usar nuestro servicio?", 0, 10, 5)

    if st.button("Enviar respuestas"):
        respuestas = [pregunta1, pregunta2, pregunta3]
        guardar_respuesta(st.session_state.current_user, respuestas)
        st.success("✅ Respuestas guardadas")
        st.balloons()

    # ---- BARRA DE PROGRESO ----
    df = cargar_datos()
    usuario_total = df[df["Usuario"] == st.session_state.current_user]["Total"].sum()
    progreso = min(usuario_total * 10, 100)
    st.progress(progreso)

    # ---- RANKING ----
    mostrar_ranking()
