
from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin import exceptions


cred = credentials.Certificate('api/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

data = {
  "Título": "Aprender, descubrir o satisfacer la curiosidad",
  "Definición": "La necesidad de satisfacer la curiosidad que permite a una persona prosperar en salud se refiere a la necesidad de obtener información y conocimientos sobre la salud y el bienestar para mejorar la calidad de vida.",
  "Objetivo": "Promover y mantener una vida saludable y satisfactoria, permitiendo la toma de decisiones informadas y la adopción de un estilo de vida más saludable y consciente",
  "Afecciones Derivadas": {
    "Falta de conocimiento sobre enfermedades y condiciones de salud": "Si las personas no pueden satisfacer su curiosidad y buscar información sobre enfermedades y condiciones de salud, corren el riesgo de no reconocer los síntomas o buscar un tratamiento temprano.",
    "Falta de conocimiento sobre las opciones de tratamiento": "Sin satisfacer su curiosidad sobre temas de salud, es posible que las personas no comprendan completamente las opciones de tratamiento disponibles.",
    "Falta de conocimiento sobre medidas preventivas": "La curiosidad por temas de salud también puede incluir preguntas sobre medidas preventivas como vacunas, lavado de manos y distanciamiento social.",
    "Mayor ansiedad y preocupación": "Cuando las personas no pueden satisfacer su curiosidad sobre temas de salud, pueden sentirse ansiosas y preocupadas por su salud y bienestar. La falta de información precisa y completa puede provocar un aumento de la ansiedad y el estrés sobre su salud."
  },
  "Cuidados por Aplicar": [
    "Evaluar el conocimiento y la comprensión de los pacientes sobre su salud y su estado de salud.",
    "Identificar las preguntas e inquietudes de los pacientes sobre su salud y sus opciones de tratamiento.",
    "Comprender la educación y las habilidades sanitarias del paciente.",
    "Proporcionar información clara, precisa y fácil de entender sobre la salud y el estado de salud de los pacientes.",
    "Asegurarse de que el paciente comprenda la información proporcionada y tenga la oportunidad de hacer preguntas.",
    "Proporcionar recursos educativos adecuados a la edad, educación y cultura del paciente. Por ejemplo, folletos, vídeos y sitios web que puedan ayudar a los pacientes a satisfacer su curiosidad.",
    "Evaluar la curiosidad y el interés de los pacientes por su salud y bienestar."
  ],
  "Img": "https://i.postimg.cc/ZBbBZSsY/14.png"
}

doc_ref = db.collection("Necesidades").document("14").collection("Aprender").document("Descripcion")
doc_ref.set(data)