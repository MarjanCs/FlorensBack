
from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin import exceptions


cred = credentials.Certificate('api/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

data = {
  "Titulo": "Desarrollo",
  "Definicion": "Se refiere al proceso de crecimiento y maduración física, cognitiva, emocional y social a lo largo de la vida.",
  "Clases": [
    {
      "Clase": "Clase 1: Crecimiento",
      "Descripcion": "Aumento de las dimensiones físicas o madurez del órgano.",
      "Diagnosticos": [
        "Esta clase actualmente no posee ningún diagnóstico"
      ]
    },
    {
      "Clase": "Clase 2: Desarrollo",
      "Descripcion": "Progreso o regresión a través de una secuencia de reconocidos hitos en la vida.",
      "Diagnosticos": [
        "00314: Retraso en el desarrollo infantil",
        "00305: Riesgo de retraso en el desarrollo infantil",
        "00315: Retraso en el desarrollo motor del lactante",
        "00316: Riesgo de retraso en el desarrollo motor infantil"
      ]
    }
  ],
  "Img": "https://i.postimg.cc/brNSkb7N/13.png"
}


doc_ref = db.collection("Dominios").document("13").collection("Desarrollo").document("Descripcion")
doc_ref.set(data)