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

def evaluar_compatibilidad(perfil, oferta): #Función para asignar un perfil y oferta laboral en el content(Promt)
  
  context.append({"role": "user", 
  "content": "Evalua la compatibilidad entre el perfil: " + perfil + ", y la siguiente oferta laboral: " + oferta}) #Input del usuario
  
  result = client.chat.completions.create(
  model="gpt-4o-mini", 
  store=True,
  messages=context
  )

  responseM = result.choices[0].message.content 
  context.append({"role":"assistant", "content":responseM}) #Guarda el mensaje dado por el modelo en la colección "context"
  return responseM
  #print("Chat:" + responseM); #Imprime la respuesta del modelo

    
#Formulario de perfil en la barra lateral
st.sidebar.title("🧑‍💼 Tu Perfil Profesional")

with st.sidebar.form("perfil_formulario"):
    nombre = st.text_input("Nombre", value="")
    experiencia = st.slider("Años de experiencia", 0, 30, 5)
    habilidades = st.text_area("Habilidades (Python, Django, SQL, etc.)", value="")
    preferencias = st.text_input("Preferencias (ej. remoto, híbrido, etc.)", value="")
    submit = st.form_submit_button("Guardar perfil")

if submit or "perfil_resumen" not in st.session_state:
    st.session_state.perfil_resumen = (
        f"{nombre}, profesional con {experiencia} años de experiencia en {habilidades}. "
        f"Busca oportunidades laborales con preferencia por modalidad {preferencias.lower()}."
    )
    st.session_state.index = 0
    st.session_state.historial = []

#Simulación de ofertas laborales
ofertas = [
    "Empresa de tecnología busca desarrollador backend con experiencia en Django y PostgreSQL. Trabajo remoto.",
    "Startup busca diseñador gráfico con conocimientos en UX/UI y herramientas como Figma y Adobe XD.",
    "Consultora requiere ingeniero de datos con experiencia en PySpark y cloud computing. Modalidad híbrida.",
    "Compañía financiera busca analista de datos con conocimientos en SQL, Power BI y Python. Trabajo presencial en CDMX.",
    "Agencia digital requiere desarrollador frontend con experiencia en React y TypeScript. Proyecto freelance.",
    "Empresa de e-commerce contrata especialista en SEO y marketing digital. Trabajo 100% remoto.",
    "Start-up de inteligencia artificial busca científico de datos con conocimientos en machine learning y TensorFlow.",
    "Organización sin fines de lucro necesita administrador de sistemas con experiencia en Linux y redes.",
    "Compañía internacional requiere DevOps con manejo de Kubernetes, Docker y CI/CD. Modalidad remota.",
    "Empresa de ciberseguridad busca pentester con certificaciones OSCP u similares. Trabajo híbrido.",
    "Multinacional busca gerente de proyecto con experiencia en metodologías ágiles (Scrum, Kanban).",
    "Fintech solicita desarrollador mobile con experiencia en Flutter o React Native. Trabajo remoto.",
    "Consultora tecnológica requiere QA tester con experiencia en pruebas automatizadas y Selenium.",
    "Startup ecológica busca community manager con conocimientos en redes sociales y herramientas de diseño.",
    "Empresa de logística contrata ingeniero en sistemas con experiencia en integración de APIs REST."
]

st.title("💼 Swipe laboral con IA")

if st.session_state.index < len(ofertas):
    oferta_actual = ofertas[st.session_state.index]
    
    st.subheader("📄 Oferta laboral")
    st.write(oferta_actual)

    if st.button("✅ Me interesa"):
        st.session_state.historial.append((oferta_actual, "interesado"))
        st.session_state.index += 1

    if st.button("❌ No me interesa"):
        st.session_state.historial.append((oferta_actual, "no interesado"))
        st.session_state.index += 1

    with st.expander("🤖 Evaluación de compatibilidad de la IA"):
        recomendacion = evaluar_compatibilidad(st.session_state.perfil_resumen, oferta_actual)
        st.write(recomendacion)

else:
    st.success("¡Has revisado todas las ofertas!")
    st.subheader("📋 Historial de tus elecciones:")
    for oferta, decision in st.session_state.historial:
        st.markdown(f"- **{decision.upper()}**: {oferta}")
