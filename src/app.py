#Se debe ejecutar en un entorno virtual con las dependencias:
#openai, streamlit y python-dotenv.

from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st

load_dotenv() #Carga las variables de .env

client = OpenAI(
  api_key= os.getenv("AI_API_KEY")#Asigna KEY
)


context = []#Aquí se almacenara los mensajes dados por el usuario y el modelo


inputU = ""
while inputU != "Terminar":
    inputU = input("Tu:")
    
    context.append({"role": "user", "content": inputU})

    result = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=context
    )

    responseM = result.choices[0].message.content
    context.append({"role":"assistant", "content":responseM})

    print("Chat:" + responseM);