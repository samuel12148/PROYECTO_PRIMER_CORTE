import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3
import threading
import time
import wave
import io
import numpy as np
from pydub import AudioSegment
from audio_recorder_streamlit import audio_recorder

# Configuración de la API de DeepSeek
API_KEY = 'sk-53751d5c6f344a5dbc0571de9f51313e'
API_URL = 'https://api.deepseek.com/v1/chat/completions'

# Prompt especializado en las novedades tecnológicas
TECH_PROMPT = """
Eres un experto en las siguientes novedades tecnológicas presentadas por Samuel Parra y Miguel Caro:

1. **NT1: Minería de Asteroides**
   - Extracción de recursos minerales de asteroides
   - Tecnologías de exploración espacial
   - Procesamiento de materiales en el espacio
   - Aspectos económicos y legales de la minería espacial

2. **NT2: Neuroprótesis Inteligentes y software libre**
   - Prótesis neurales con inteligencia artificial
   - Sistemas de control mediante señales cerebrales
   - Plataformas de software libre para neuroprótesis
   - Interfaces hombre-máquina avanzadas

3. **NT3: Interfaz Cerebro-Computador No Invasivas de Alta Resolución y el uso de los sistemas digitales en esta tecnología**
   - BCIs (Brain-Computer Interfaces) no invasivas
   - Técnicas de EEG de alta resolución
   - Procesamiento digital de señales cerebrales
   - Aplicaciones médicas y de rehabilitación
   - Sistemas digitales para amplificación y filtrado de señales

Responde de manera técnica pero clara, proporcionando información precisa sobre estos temas.
Si la pregunta no está relacionada con estas tecnologías, indica amablemente que solo puedes hablar de estos temas específicos.
"""

def enviar_mensaje(mensaje):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': TECH_PROMPT},
            {'role': 'user', 'content': mensaje}
        ],
        'temperature': 0.7,
        'max_tokens': 400
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Inicializar el motor de texto a voz
def init_tts_engine():
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        # Configurar voz en español si está disponible
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'español' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 150)  # Velocidad de habla
        return engine
    except:
        return None

# Función para hablar en un hilo separado
def speak_text(engine, text):
    if not engine:
        return None
        
    def speak():
        engine.say(text)
        engine.runAndWait()
    
    thread = threading.Thread(target=speak)
    thread.start()
    return thread

# Función para mejorar la calidad del audio
def improve_audio_quality(audio_bytes):
    try:
        # Convertir bytes a AudioSegment
        audio = AudioSegment.from_wav(io.BytesIO(audio_bytes))
        
        # Reducir el volumen para evitar saturación (ajustar según necesidad)
        audio = audio - 5  # Reducir 5 dB
        
        # Aplicar compresión para reducir picos de volumen
        audio = audio.compress_dynamic_range()
        
        # Convertir de vuelta a bytes
        buffer = io.BytesIO()
        audio.export(buffer, format="wav")
        return buffer.getvalue()
    except:
        # Si hay error, devolver el audio original
        return audio_bytes

# Función para transcribir audio con múltiples intentos
def transcribe_audio(audio_bytes, attempts=3):
    recognizer = sr.Recognizer()
    
    # Mejorar la calidad del audio
    improved_audio = improve_audio_quality(audio_bytes)
    
    # Convertir bytes a AudioData
    audio_data = sr.AudioData(improved_audio, sample_rate=44100, sample_width=2)
    
    for attempt in range(attempts):
        try:
            # Usar el reconocimiento de Google
            text = recognizer.recognize_google(audio_data, language='es-ES')
            return text, True
        except sr.UnknownValueError:
            if attempt == attempts - 1:
                return "No se pudo entender el audio. Por favor, habla más claro o más cerca del micrófono.", False
        except sr.RequestError as e:
            if attempt == attempts - 1:
                return f"Error en el servicio de reconocimiento: {e}", False
        time.sleep(0.5)  # Pequeña pausa entre intentos
    
    return "Error desconocido en el reconocimiento de voz", False

# ------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ------------------------------
st.set_page_config(
    page_title="Chatbot de Voz - Novedades Tecnológicas",
    page_icon="🎙️",
    layout="wide"
)

# ------------------------------
# ESTILOS CSS
# ------------------------------
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    
    /* Texto blanco para la interfaz */
    .stApp, h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #FFFFFF !important;
    }
    
    /* Chat messages con fondo claro y texto negro */
    .stChatMessage {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
    }
    
    /* Texto negro para las respuestas del chat */
    .stChatMessage p, .stChatMessage div, .stChatMessage span {
        color: #000000 !important;
    }
    
    /* Botones visibles */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        margin: 5px;
    }
    
    /* Estilo para el grabador de audio */
    .audio-recorder {
        background-color: #FF4B4B;
        border-radius: 50%;
        margin: 10px auto;
        display: block;
    }
    
    /* Panel de consejos */
    .tips-panel {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 15px 0;
    }
    
    /* Opciones de entrada */
    .input-option {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# INICIALIZACIÓN DEL MOTOR DE TEXTO A VOZ
# ------------------------------
if 'tts_engine' not in st.session_state:
    st.session_state.tts_engine = init_tts_engine()

# ------------------------------
# TÍTULO Y AUTORES
# ------------------------------
st.title("🎙️ Chatbot de Voz - Novedades Tecnológicas")
st.markdown("### Presentado por: **Samuel Parra & Miguel Caro**")

st.write("---")

# ------------------------------
# VIDEO DE YOUTUBE
# ------------------------------
st.header("🎥 Video Relacionado")
st.markdown("### Conoce más sobre estas tecnologías a través de este video")

# Insertar el video de YouTube
video_url = "https://www.youtube.com/watch?v=mBGIwmC7NBk"
st.video(video_url)

st.write("---")

# ------------------------------
# CONSEJOS PARA MEJORAR EL RECONOCIMIENTO DE VOZ
# ------------------------------
with st.expander("💡 Consejos para mejorar el reconocimiento de voz", expanded=True):
    st.markdown("""
    <div class="tips-panel">
    <h4>Si el micrófono se satura o no te entiende:</h4>
    <ul>
        <li>🎤 Habla claro y a un volumen moderado</li>
        <li>📏 Mantén una distancia de 15-30 cm del micrófono</li>
        <li>🔇 Reduce el ruido ambiental</li>
        <li>🐢 Habla un poco más lento de lo normal</li>
        <li>🎧 Usa audífonos con micrófono para mejor calidad</li>
        <li>🔄 Si no funciona, usa la opción de texto en lugar de voz</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------
# NOVEDADES TECNOLÓGICAS
# ------------------------------
st.header("📋 Temas de la Exposición")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🪐 NT1: Minería de Asteroides")
    st.markdown("""
    - Extracción de recursos minerales
    - Exploración espacial avanzada
    - Procesamiento in-situ
    - Aspectos legales y económicos
    """)

with col2:
    st.subheader("🧠 NT2: Neuroprótesis Inteligentes")
    st.markdown("""
    - IA en prótesis neurales
    - Control por señales cerebrales
    - Software libre médico
    - Interfaces hombre-máquina
    """)

with col3:
    st.subheader("📊 NT3: Interfaces Cerebro-Computador")
    st.markdown("""
    - BCIs no invasivas
    - EEG de alta resolución
    - Procesamiento digital
    - Aplicaciones médicas
    """)

st.write("---")

# ------------------------------
# CHATBOT ESPECIALIZADO CON VOZ
# ------------------------------
st.header("💬 Chatbot con Reconocimiento de Voz")
st.markdown("### Elige cómo quieres interactuar:")

# Opciones de entrada
input_option = st.radio(
    "Método de entrada:",
    ["🎤 Usar voz (recomendado)", "⌨️ Usar texto"],
    horizontal=True
)

# Inicializar historial de chat
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "¡Hola! Soy tu asistente especializado en las novedades tecnológicas presentadas por Samuel Parra y Miguel Caro. Puedes hablarme o escribirme sobre:\n\n- 🪐 Minería de Asteroides\n- 🧠 Neuroprótesis Inteligentes\n- 📊 Interfaces Cerebro-Computador\n\n¿Sobre qué tema te gustaría saber más?"
    })

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])
    else:
        with st.chat_message("user"):
            st.markdown(message["content"])

# ------------------------------
# ENTRADA POR VOZ
# ------------------------------
if input_option == "🎤 Usar voz (recomendado)":
    st.markdown("### 🎤 Grabar audio")
    st.markdown("Haz clic en el micrófono para grabar tu pregunta por voz (máximo 10 segundos)")
    
    # Grabador de audio con duración limitada
    audio_bytes = audio_recorder(
        text="",
        recording_color="#FF4B4B",
        neutral_color="#6C757D",
        icon_name="microphone",
        icon_size="2x",
        pause_threshold=10,  # Limitar a 10 segundos
    )

    # Procesar audio grabado
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        with st.spinner("Mejorando calidad de audio y transcribiendo..."):
            transcribed_text, success = transcribe_audio(audio_bytes)
            
            if success:
                # Mostrar texto transcrito
                st.success(f"Texto transcrito: {transcribed_text}")
                
                # Agregar mensaje de usuario al historial
                st.session_state.messages.append({"role": "user", "content": transcribed_text})
                
                # Mostrar mensaje de usuario
                with st.chat_message("user"):
                    st.markdown(f"**{transcribed_text}**")
                
                # Generar respuesta
                with st.spinner("Buscando información especializada..."):
                    respuesta = enviar_mensaje(transcribed_text)
                
                # Mostrar respuesta
                with st.chat_message("assistant"):
                    st.markdown(respuesta)
                
                # Guardar respuesta en historial
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
                
                # Reproducir respuesta por voz si el motor TTS está disponible
                if st.session_state.tts_engine:
                    with st.spinner("Generando respuesta de voz..."):
                        speak_text(st.session_state.tts_engine, respuesta)
                        st.success("Respuesta de voz generada")
                else:
                    st.warning("El motor de texto a voz no está disponible")
            else:
                st.error(transcribed_text)
                st.info("Puedes intentarlo de nuevo o usar la opción de texto a continuación")

# ------------------------------
# ENTRADA DE TEXTO (alternativa)
# ------------------------------
st.markdown("### ⌨️ Escribir pregunta")
pregunta = st.chat_input("Escribe tu pregunta sobre las novedades tecnológicas...")

if pregunta:
    # Agregar mensaje de usuario al historial
    st.session_state.messages.append({"role": "user", "content": pregunta})
    
    # Mostrar mensaje de usuario
    with st.chat_message("user"):
        st.markdown(f"**{pregunta}**")
    
    # Generar respuesta
    with st.spinner("Buscando información especializada..."):
        respuesta = enviar_mensaje(pregunta)
    
    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(respuesta)
    
    # Guardar respuesta en historial
    st.session_state.messages.append({"role": "assistant", "content": respuesta})
    
    # Reproducir respuesta por voz si el motor TTS está disponible
    if st.session_state.tts_engine:
        with st.spinner("Generando respuesta de voz..."):
            speak_text(st.session_state.tts_engine, respuesta)
            st.success("Respuesta de voz generada")
    else:
        st.warning("El motor de texto a voz no está disponible")

# ------------------------------
# BOTONES DE CONTROL
# ------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    # Botón para repetir última respuesta en voz
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        if st.button("🔊 Repetir última respuesta en voz", use_container_width=True):
            if st.session_state.tts_engine:
                with st.spinner("Reproduciendo respuesta..."):
                    speak_text(st.session_state.tts_engine, st.session_state.messages[-1]["content"])
                    st.success("Respuesta reproducida")
            else:
                st.warning("El motor de texto a voz no está disponible")

with col2:
    # Botón para probar el micrófono
    if st.button("🎤 Probar micrófono", use_container_width=True):
        st.info("Graba un audio de prueba para verificar la calidad. Di tu nombre o una frase simple.")
        test_audio = audio_recorder(
            text="",
            recording_color="#4CAF50",
            neutral_color="#6C757D",
            icon_name="microphone",
            icon_size="2x",
            pause_threshold=5,
        )
        
        if test_audio:
            st.audio(test_audio, format="audio/wav")
            st.success("Audio grabado correctamente. Ahora puedes usarlo en el chat principal.")

with col3:
    # Botón para limpiar chat
    if st.button("🧹 Limpiar Conversación", use_container_width=True):
        st.session_state.messages = [{
            "role": "assistant", 
            "content": "¡Conversación limpiada! ¿Sobre qué novedad tecnológica te gustaría hablar?"
        }]
        st.rerun()

# ------------------------------
# FOOTER
# ------------------------------
st.write("---")
st.markdown("""
<div style='text-align: center; color: #FFFFFF !important;'>
    <p><strong>Chatbot de Voz - Novedades Tecnológicas - Samuel Parra & Miguel Caro</strong></p>
    <p>Proyecto Digitales III - Universidad Santo Tomás</p>
</div>
""", unsafe_allow_html=True)
