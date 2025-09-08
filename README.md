#  Proyecto Digitales III

Este proyecto integra robótica y desarrollo de software para exponer sobre tres innovaciones tecnológicas:  

-  Minería de Asteroides  
-  Neuroprótesis Inteligentes  
-  Interfaces Cerebro-Computador (BCI)  

La exposición fue realizada por el robot **Pepper**, acompañado de una serie de diapositivas creadas en *Gamma*. Además, se desarrolló un **Dashboard interactivo con Streamlit** que permite visualizar los videos de Pepper, observar una breve descripción de los temas a exponer y simular la interacción con un chatbot.

##  Proceso de desarrollo

1. **Creación de diapositivas**  
   - Se diseñaron en la plataforma [Gamma](https://gamma.app/).  
   - Incluyen la información investigada sobre cada tema.  

2. **Programación de Pepper**  
   - Se elaboró un script en Python que controla la voz, movimientos y pantalla del robot.  
   - Pepper presentó los tres temas de forma interactiva.  

3. **Construcción del Dashboard**  
   - Se creó una aplicación con **Streamlit** que integra:  
     - Video de la exposición de Pepper.  
     - Secciones con descripciones de cada innovación.  
     - Un chatbot simulado para consultas.  

---

## 🚀 Cómo ejecutar el Dashboard

### 1. Clonar el repositorio
git clone https://github.com/TuUsuario/ProyectoPepper.git

cd ProyectoPepper
### 2. instalar dependencias
pip install streamlit
### 3. Ejecutar la app
streamlit run app.py
