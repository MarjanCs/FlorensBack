
from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin import exceptions


cred = credentials.Certificate('api/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

data = {
  "Titulo": "Valores",
  "Definicion": "Se centra en creencias, valores y perspectivas de la vida y describe cómo afectan la salud física y mental, y cómo se pueden ajustar o cambiar para mejorar la salud.",
  "Valoraciones": {
    "Prácticas religiosas, creencias y tradiciones culturales": "Influencia en la salud y cómo se alinean con las expectativas del paciente.",
    "Metas y logros personales, satisfacción con la vida actual": "Impacto en la salud y bienestar del individuo.",
    "Conflictos en valores, creencias y expectativas relacionadas con la salud": "Identificación de discrepancias que afectan las decisiones de tratamiento."
  },
  "Alteraciones": [
    "Conflictos con creencias personales o prácticas religiosas.",
    "Problemas con la práctica religiosa o conflictos con valores.",
    "Preocupación por el significado de la vida, la muerte, el dolor o la enfermedad.",
    "Eventos que afectan los valores personales, como pérdida de función, enfermedad mortal o la muerte de un ser querido."
  ],
  "Resultados": [
    "Apoyo religioso/espiritual influyente en la salud del paciente durante la enfermedad.",
    "Conflicto cultural o de valores: discrepancias entre creencias y prácticas médicas/familiares que impactan en decisiones de tratamiento.",
    "El impacto de las creencias en la percepción de la enfermedad, las expectativas de recuperación y tratamiento.",
    "Falta de apoyo social que dificulta la adaptación a la enfermedad y recuperación.",
    "Percepciones diversas sobre curación y muerte, desde aceptación hasta negación del proceso."
  ],
  "Img": "https://i.postimg.cc/50dCv1GT/11.png"
}


doc_ref = db.collection("Patrones").document("11").collection("Valores").document("Descripcion")
doc_ref.set(data)