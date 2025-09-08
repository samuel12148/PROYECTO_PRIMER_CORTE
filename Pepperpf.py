import streamlit as st
import requests

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

# ------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ------------------------------
st.set_page_config(
    page_title="Novedades Tecnológicas - Samuel Parra & Miguel Caro",
    page_icon="🚀",
    layout="wide"
)

# ------------------------------
# ESTILOS CSS PARA TEMA OSCURO CON RESPUESTAS EN NEGRO
# ------------------------------
st.markdown("""
<style>
    /* Fondo oscuro para toda la aplicación */
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
    
    /* Input field visible */
    .stTextInput>div>div>input {
        color: #000000;
        background-color: #ffffff;
        border: 2px solid #4CAF50;
    }
    
    /* Botones visibles */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    
    /* Expandidores visibles */
    .stExpander {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        margin: 10px 0;
        background-color: #0E1117;
    }
    
    /* Encabezados de expandidores en blanco */
    .stExpander label p {
        color: #FFFFFF !important;
        font-weight: bold;
    }
    
    /* Ajustes para el video */
    .video-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# TÍTULO Y AUTORES
# ------------------------------
st.title("🚀 Novedades Tecnológicas")
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
# CHATBOT ESPECIALIZADO
# ------------------------------
st.header("💬 Chatbot Especializado")
st.markdown("### Pregunta sobre cualquiera de las tres novedades tecnológicas")

# Inicializar historial de chat
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "¡Hola! Soy tu asistente especializado en las novedades tecnológicas presentadas por Samuel Parra y Miguel Caro. Puedo responderte sobre:\n\n- 🪐 Minería de Asteroides\n- 🧠 Neuroprótesis Inteligentes\n- 📊 Interfaces Cerebro-Computador\n\n¿Sobre qué tema te gustaría saber más?"
    })

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])
    else:
        with st.chat_message("user"):
            st.markdown(message["content"])

# Input de pregunta
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

# ------------------------------
# EJEMPLOS DE PREGUNTAS
# ------------------------------
st.write("---")
st.header("💡 Ejemplos de Preguntas")

ejemplos_col1, ejemplos_col2, ejemplos_col3 = st.columns(3)

with ejemplos_col1:
    st.markdown("**🪐 Minería de Asteroides**")
    st.markdown("""
    - ¿Qué minerales se pueden extraer?
    - ¿Cómo funciona la minería espacial?
    - ¿Qué tecnologías se usan?
    - ¿Es legal la minería de asteroides?
    """)

with ejemplos_col2:
    st.markdown("**🧠 Neuroprótesis Inteligentes**")
    st.markdown("""
    - ¿Cómo funcionan las neuroprótesis?
    - ¿Qué software libre se usa?
    - ¿Qué ventajas tienen?
    - ¿Qué aplicaciones médicas tienen?
    """)

with ejemplos_col3:
    st.markdown("**📊 Interfaces Cerebro-Computador**")
    st.markdown("""
    - ¿Qué es un BCI no invasivo?
    - ¿Cómo procesan las señales cerebrales?
    - ¿Qué sistemas digitales se usan?
    - ¿Qué resolución pueden alcanzar?
    """)

# ------------------------------
# BOTÓN PARA LIMPIAR CHAT
# ------------------------------
if st.button("🧹 Limpiar Conversación"):
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
    <p><strong>Novedades Tecnológicas - Samuel Parra & Miguel Caro</strong></p>
    <p>Proyecto Digitales III - Universidad Santo Tomás</p>
</div>
""", unsafe_allow_html=True)
