import os
import logging
import openai
import google.generativeai as genai
import markdown2
import time
from abc import ABC, abstractmethod
from .models import Menu

# Configuración básica del logging
logging.basicConfig(level=logging.INFO)

# Función para crear un plato
def CrearPlato(descrip: str, titulo: str):
    """Crea un nuevo plato en el menú con la descripción y el título proporcionados."""
    Menu.objects.create(
        title=titulo,
        descripcion=descrip,
        imagen="menu/images/vaca_marina.png"
    )

# Interfaz para generadores de texto
class TextGenerationInterface(ABC):
    @abstractmethod
    def generate_content(self, prompt: str) -> str:
        pass

# Implementación de la interfaz usando OpenAI
class OpenAITextGenerator(TextGenerationInterface):
    def __init__(self):
        openai.api_key = "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"  
    
    def preparar_mensajes(self, prompt: str) -> list:
        """Prepara los mensajes que se enviarán a la API."""
        inicial = (
            "Vas a actuar como un experto en recetas de todo tipo. Debes brindar información sobre cosas como la "
            "cantidad de personas, alergias, tipo de situación, posibles ingredientes a disposición, entre otros. "
            "Genera un menú con la siguiente información: "
        )
        mensaje1 = inicial + prompt + " Si necesitas más información, no la preguntes, solamente genera el menú cumpliendo lo solicitado."
        return [{"role": "user", "content": mensaje1}]
    
    def obtener_respuesta(self, mensajes: list) -> str:
        """Envía los mensajes a la API y retorna la respuesta."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=mensajes
            )
            return response['choices'][0]['message']['content']
        except openai.error.OpenAIError as e:
            logging.error("Error de OpenAI: %s", e)
            return "Error al comunicarme con OpenAI."
    
    def generate_content(self, prompt: str) -> str:
        """Genera contenido basado en el prompt proporcionado."""
        mensajes = self.preparar_mensajes(prompt)
        respuesta = self.obtener_respuesta(mensajes)

        # Crear el título del plato
        mensajes.append({"role": "assistant", "content": respuesta})
        titulo = "Ahora limítate a decirme el título del platillo basado en lo que me acabas de decir, sin utilizar letra en negrilla:"
        mensajes.append({"role": "user", "content": titulo})
        
        respuesta_final = self.obtener_respuesta(mensajes)
        
        # Crear un plato a partir de las respuestas
        CrearPlato(respuesta, respuesta_final)
        
        return markdown2.markdown(respuesta)

# Implementación de la interfaz usando Gemini
class GeminiTextGenerator(TextGenerationInterface):
    def __init__(self):
        genai.configure(api_key="AIzaSyB5DIgYTBVipSNGwLfAK-RR470u3cEFIlI")  # Cargar clave de API desde variables de entorno

    def preparar_mensajes(self, prompt: str) -> str:
        """Prepara los mensajes que se enviarán a la API."""
        inicial = (
            "Vas a actuar como un experto en recetas de todo tipo. Debes brindar información sobre cosas como la "
            "cantidad de personas, alergias, tipo de situación, posibles ingredientes a disposición, entre otros. "
            "Genera un menú con la siguiente información: "
        )
        return inicial + prompt + " Si necesitas más información, no la preguntes, solamente genera el menú cumpliendo lo solicitado."
    
    def obtener_respuesta(self, mensaje: str) -> str:
        """Envía un mensaje a la API de Gemini y retorna la respuesta."""
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        
        retorno = model.generate_content(mensaje)
        return retorno.candidates[0].content.parts[0].text
    
    def generate_content(self, prompt: str) -> str:
        """Genera contenido utilizando la API de Gemini basado en el prompt."""
        mensaje1 = self.preparar_mensajes(prompt)
        retorno_text = self.obtener_respuesta(mensaje1)
        
        time.sleep(2)  # Controlar la tasa de solicitudes
        titulo = self.obtener_respuesta("Ahora limítate a decirme el título del platillo basado en lo que me acabas de decir, sin utilizar letra en negrilla:" + retorno_text)
        
        # Crear un plato a partir de las respuestas
        CrearPlato(retorno_text, titulo)
        
        return markdown2.markdown(retorno_text)
