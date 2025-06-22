import streamlit as st
from groq import Groq

#Esta funcion es para; el título, el icono de la pestaña y
# para que el texto este centrado
st.set_page_config(page_title="Mi chatbot", page_icon="🦁", layout="centered")

#Título de la app
st.title("¡Gracias por visitar mi primera aplicación con Streamlit!")

#Variable que guarda el nombre del usuario que saludaremos
nombre = st.text_input("¿Cuál es tu nombre?: ")

if st.button("Saludar"):
    st.write(f"¡Hola, {nombre}! Bienvenido/a a mi chatbot")

modelos = ["llama3-8b-8192", "llama3-70b-8192", "gemma2-9b-it"]

#Clase 7
def configurar_pagina():
    st.title("Mi chat") 
    st.sidebar.title("Configuración de la IA") #cuando aparezca el widget que tmb aparezca el titulo. Con widget me refiero al rectangulo gris a la izquierda como un menu lateral izq

    elegirModelo = st.sidebar.selectbox("Elegí un modelo", options=modelos, index=0) #Variable que guarda el elemneto/sidebar/el widget..
    #..para que el usuario elija. index=0 quiere decir que el primer modelo, elemento coincida con la posicion cero de la lista modelos
    return elegirModelo 

#Haremos que nuestro chatbot conecte con groq a traves de la API, y tenga disponible los modelos de la variable configurar_pagina()
#Función que nos ayuda a conectar con Groq

def crear_usuario_groq():
    claveSecreta = st.secrets["clave_api"] #buscará la clave API que esta en nuestro archivo secrets.toml
    return Groq(api_key=claveSecreta) #aca se confirma que el usuario se pudo crear una cuenta y de que puede usar los permisos que tiene groq

#Configurar el modelo y el mensaje del usuario
#Esta función tomará el modelo que eligió el usuario y el mensaje y me de una respuesta
#Esta funcion NO da respuesta. Solo le informa al modelo de IA la que el usuario quiere (osea le informa su mensaje y el modelo que eligió) como si esa función fuera un camarero y dice "el mensaje del usuario fue tal.. y el modelo que eligió fue tal.."

def configurar_modelo(cliente, modelo, mensajeDeEntrada): #3 parametros, cliente hace referencia al usuario, modelo hace referencia al modelo que el usuario eligió, y mensajeDeEntrada hace referencia al mensaje que el usuario escribio en el chatbot, es lo que queremos que el modelo de IA lea y responda
    return cliente.chat.completions.create(
        model=modelo, #indica que modelo eligió el usuario
        messages = [{"role":"user", "content":mensajeDeEntrada}], #lista q tiene 2 elementos, role-user hace referiencia a quien hace la preguna y es el usuario, y lo otro toma como valor el input del mensaje que esta mas arriba que es lo que el usuario va a escribir
        stream = True #que lo interprete en tiempo real y..
        #.. escribe la respuesta apenas la tiene
    )

#Función que guarda el historial de mensajes que tiene el usuario con el chatbot
#Funcion que es como un caché 

def inicializar_estado():
    if "mensajes" not in st.session_state: #comprueba si tenemos una lista que guarda los mensajes que envió el usuario
        st.session_state.mensajes = [] #si no existe esa lista, se creará una vacía y guarda los mensajes del usuario y las respuestas del chatbot y que se vea un HISTORIAL en nuestra interfaz 

#Clase 8
#Actualizar historial 
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role":rol, "content":contenido , "avatar": avatar})

#Mostar Hisotiral 
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

#Area Historial 
def area_chat():
    contenedorDelChat = st.container(height=350, border=True)
    with contenedorDelChat:
        mostrar_historial()

#Clase 9
#Generar repuesta (voy a capturar la respuesta del modelo)
def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()

    mensaje = st.chat_input("Escribí tu mensaje") #variable que hace que el usuario mande un mensaje
    if mensaje: #comprueba si hay un mensaje dentro de la variable "mensaje"
        actualizar_historial("user", mensaje, "🧑")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo: #
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                #se escribe la respuesta del chatbot
                actualizar_historial("assistant", respuesta_completa, "🤖") #muestra quien esta hablando; el bot, y su respuesta y su avatar (osea su emoji que nos indica que esta hablando el bot)
            
            st.rerun()

#Aca nos aseguramos de que nuestro archivo se ejecute unicamente..
#.. cuando se ejecuta directamente y no cuando es importado como una librería
if __name__ == "__main__":
    main()

    