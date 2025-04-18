import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import html

# Cargar API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Estilo visual tipo burbuja
st.markdown("""
    <style>
    .mensaje-usuario {
        background-color: #d4edda;
        color: #000;
        padding: 12px;
        border-radius: 10px;
        margin: 5px 0;
        width: fit-content;
        max-width: 80%;
        margin-left: auto;
    }
    .mensaje-bot {
        background-color: #f1f1f1;
        color: #000;
        padding: 12px;
        border-radius: 10px;
        margin: 5px 0;
        width: fit-content;
        max-width: 80%;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("💬 Chat IA - Asistente de Carlos")

# Botón para resetear conversación
if st.button("🧹 Resetear conversación"):
    st.session_state.mensajes = [
        {"role": "system", "content": "Eres un asistente útil y conversacional."}
    ]
    st.success("✅ Conversación reiniciada.")

# Inicializar historial
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "system", "content": "Eres un asistente útil y conversacional."}
    ]

# Formulario con input
with st.form("formulario_pregunta", clear_on_submit=True):
    pregunta = st.text_input("Escribe tu mensaje:")
    enviado = st.form_submit_button("Enviar")

# Procesar pregunta
if enviado and pregunta:
    st.session_state.mensajes.append({"role": "user", "content": pregunta})

    with st.spinner("Pensando..."):
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.mensajes
        )
        texto_respuesta = respuesta.choices[0].message.content.strip()
        st.session_state.mensajes.append({"role": "assistant", "content": texto_respuesta})

# Mostrar historial visual
if len(st.session_state.mensajes) > 1:
    st.markdown("---")
    st.subheader("📝 Conversación")
    for mensaje in st.session_state.mensajes[1:]:  # omitir el 'system'
        clase = "mensaje-usuario" if mensaje["role"] == "user" else "mensaje-bot"
        contenido = html.escape(mensaje["content"])
        st.markdown(f"<div class='{clase}'>{contenido}</div>", unsafe_allow_html=True)

