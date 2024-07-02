#Importacion de libreria para la creación de rutas
from flask import Flask, jsonify, request
#importacion de libreria para el uso de cors en el sistema
from flask_cors import CORS
#Importacion de librerias para el uso de firebase
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin import exceptions
#Importacion de la libreria para el uso de la IA de Google
import google.generativeai as genai

#Configuracion de la Clave para el uso de la IA de Google
genai.configure(api_key="AIzaSyB43im5LCSxDuV1iLa96jugVafw43gbRJs")
#Configurar el modelo de red neuronal para el uso de la IA
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
chat

app = Flask(__name__)
CORS(app)

# Configurar la conexión con Firebase
cred = credentials.Certificate('api/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Ruta para obtener todos los elementos
@app.route('/Necesidades', methods=['GET'])
def get_items():
    items = db.collection('Necesidades').document("13").collection("Ocio")
    print(items)
    item_list = [item.to_dict() for item in items.get()]
    return jsonify(item_list)


# Ruta para registrar usuario
@app.route('/Registro', methods=['POST'])
def add_User():
    datos_user = request.get_json()
    new_user = auth.create_user(
        email=datos_user['email'],
        password=datos_user['password']
    )
    doc_ref = db.collection('usuarios').document(new_user.uid)
    doc_ref.set({
        'nombre': datos_user['nombre'],
        'pais': datos_user['pais'],
        'contrasenia': datos_user['password'],
        'ciudad': datos_user['ciudad'],
        'universidad': datos_user['universidad'],
        'rol': datos_user['rol']
    })
    return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

# Ruta para inicio de Sesión
@app.route('/verificar_usuario', methods=['POST'])
def verificar_usuario():
    datos_solicitud = request.get_json()
    email = datos_solicitud['email']
    contrasena = datos_solicitud['password']

    try:
        # Obtener información del usuario por correo electrónico
        usuario = auth.get_user_by_email(email)
        #print(usuario.uid)
        informacion_adicional_ref = db.collection('usuarios').document(usuario.uid)
        informacion_adicional = informacion_adicional_ref.get().to_dict()
        #print(informacion_adicional['contrasenia'])
        # Si no se produce una excepción, el usuario existe
        if contrasena == informacion_adicional['contrasenia']:
            return jsonify({"status": True,"mensaje": "Usuario existe","rol":informacion_adicional['rol'],"usuario":usuario.uid},), 200
        else:
            return jsonify({"status": False,"mensaje": "Contraseña Incorrecta"}), 404

    except exceptions.FirebaseError as e:
        # Si hay un error de autenticación, verificar el tipo de error
        return jsonify({"mensaje": "Usuario no encontrado","status": False,}), 404

#### Bibliografias
@app.route('/BibliografiasList/<string:nombre_documento>', methods=['GET'])
def get_Bibliografia(nombre_documento):
    try:
        informacion_adicional_ref = db.collection('Bibliografia').document(nombre_documento)
        documento = informacion_adicional_ref.get()
        if documento.exists:
            datos_documento = documento.to_dict()
            return jsonify({"Bibliografias": datos_documento, "status": True})
        else:
            return jsonify({"mensaje": f'Documento {nombre_documento} no encontrado', "status": False}), 404
    except Exception as e:
        return jsonify({"mensaje": f'Error al obtener la información: {e}', "status": False}), 500

####Ruta par guardar las bibliografias
@app.route('/EditarDocumentBibliografia/', methods=['POST'])    
def crear_Bibliografia():
    datos_solicitud = request.get_json()
    Bibliografia = datos_solicitud['UpdateBibliografia']
    print(Bibliografia)
    NombreDocument = datos_solicitud['Name']
    try:
        doc_ref = db.collection("Bibliografia").document(NombreDocument)
        resultado = doc_ref.set(Bibliografia)
        if resultado.update_time:
            return jsonify({"status": True,"mensaje": "Informacion actualizada en Necesidades en la Bibliografia"}), 200
        else:
            return jsonify({"status": False,"mensaje": "Problema al actualizar las nuevas Bibliografias"}), 404

    except exceptions.FirebaseError as e:
        # Si hay un error de autenticación, verificar el tipo de error
        return jsonify({"mensaje": "Usuario no encontrado","status": False,}), 404


### Necesidades
@app.route('/NecesidadesLista', methods=['GET'])
def get_NecesidadesLista():
    items = db.collection('Necesidades').stream()
    print(items)
    datos_coleccion = {}
    for i, doc in enumerate(items):
            # Usar el índice como ID comenzando desde 1
            identificador = str(i + 1)
            datos = doc.to_dict()
            datos["Id"] = doc.id
            datos_coleccion[identificador] = datos
    return jsonify(datos_coleccion)
#Ruta para obtener una información Necesidades
@app.route('/DocNecesidadesInfo', methods=['POST'])
def get_NecesidadesDocInfo():
    datos_solicitud = request.get_json()
    doc = datos_solicitud['Document']
    nameCollection = datos_solicitud['Name']
    try:
        informacion_adicional_ref = db.collection('Necesidades').document(doc).collection(nameCollection)
        item_list = [item.to_dict() for item in informacion_adicional_ref.get()]
        return jsonify(item_list)
    except Exception as e:
        return jsonify({"mensaje": "Error al obtener la Información","status": False,}), 404
    
@app.route('/EditarDocumentNecesidades/<string:nombre_documento>/<string:nombre_colleccion>', methods=['PUT'])
def get_EditarParametros(nombre_documento, nombre_colleccion):
    datos_solicitud = request.get_json()
    Definicion = datos_solicitud ['DefinicionUpdate']
    Titulo = datos_solicitud ['TituloUpdate']
    Objetivo = datos_solicitud ['ObjetivoUpdate']
    Afecciones = datos_solicitud ['AfeccionesUpdate']
    Cuidados = datos_solicitud ['CuidadosUpdate']
    print(Definicion+"/*"+Titulo+"/*"+Objetivo)
    try:
        informacion_adicional_ref = db.collection('Necesidades').document(nombre_documento).collection(nombre_colleccion).document("Descripcion")
        documento_actual = informacion_adicional_ref.get()
        
        if documento_actual.exists:
            informacion_adicional_ref.update({"Objetivo": Objetivo,"Titulo": Titulo,"Definicion": Definicion,"Afecciones":Afecciones,"Cuidados":Cuidados})
            documento_actualizado = informacion_adicional_ref.get().to_dict()

            return jsonify({"mensaje": f'Documento {nombre_documento} actualizado', "datos": documento_actualizado, "status": True})
        else:
            return jsonify({"mensaje": f'Documento {nombre_documento} no encontrado',"status": False}), 404

    except Exception as e:
        print(e)
        return jsonify({"error": f'Error al editar el documento: {e}',"status": False}), 500

###Dominios
@app.route('/DominiosLista', methods=['GET'])
def get_DominiosLista():
    items = db.collection('Dominios').stream()
    print(items)
    datos_coleccion = {}
    for i, doc in enumerate(items):
            # Usar el índice como ID comenzando desde 1
            identificador = str(i + 1)
            datos = doc.to_dict()
            datos["Id"] = doc.id
            datos_coleccion[identificador] = datos
    return jsonify(datos_coleccion)

#Ruta para obtener una información dominios
@app.route('/DocDominiosInfo', methods=['POST'])
def get_DominiosDocInfo():
    datos_solicitud = request.get_json()
    doc = datos_solicitud['Document']
    nameCollection = datos_solicitud['Name']
    try:
        informacion_adicional_ref = db.collection('Dominios').document(doc).collection(nameCollection)
        item_list = [item.to_dict() for item in informacion_adicional_ref.get()]
        return jsonify(item_list)
    except Exception as e:
        return jsonify({"mensaje": "Error al obtener la Información","status": False,}), 404



###Patrones
@app.route('/PatronesLista', methods=['GET'])
def get_PatronesLista():
    items = db.collection('Patrones').stream()
    print(items)
    datos_coleccion = {}
    for i, doc in enumerate(items):
            # Usar el índice como ID comenzando desde 1
            identificador = str(i + 1)
            datos = doc.to_dict()
            datos["Id"] = doc.id
            datos_coleccion[identificador] = datos
    return jsonify(datos_coleccion)

#Ruta para obtener una informacion Patrones
@app.route('/DocPatronesInfo', methods=['POST'])
def get_PatronesDocInfo():
    datos_solicitud = request.get_json()
    doc = datos_solicitud['Document']
    nameCollection = datos_solicitud['Name']
    try:
        informacion_adicional_ref = db.collection('Patrones').document(doc).collection(nameCollection)
        print(nameCollection)
        item_list = [item.to_dict() for item in informacion_adicional_ref.get()]
        return jsonify(item_list)
    except Exception as e:
        return jsonify({"mensaje": "Error al obtener la Información","status": False,}), 404
    
@app.route('/EditarDocumentDominio/<string:nombre_documento>/<string:nombre_colleccion>', methods=['PUT'])
def get_EditarDominios(nombre_documento, nombre_colleccion):
    datos_solicitud = request.get_json()
    Definicion = datos_solicitud ['DefinicionUpdate']
    Titulo = datos_solicitud ['TituloUpdate']
    Clases = datos_solicitud ['ClasesUpdate']
    try:
        informacion_adicional_ref = db.collection('Dominios').document(nombre_documento).collection(nombre_colleccion).document("Descripcion")
        documento_actual = informacion_adicional_ref.get()
        
        if documento_actual.exists:
            informacion_adicional_ref.update({"Titulo": Titulo,"Definicion": Definicion,"Clases":Clases})
            documento_actualizado = informacion_adicional_ref.get().to_dict()
            print(documento_actualizado)
            return jsonify({"mensaje": f'Documento {nombre_documento} actualizado', "datos": documento_actualizado, "status": True})
        else:
            return jsonify({"mensaje": f'Documento {nombre_documento} no encontrado',"status": False}), 404

    except Exception as e:
        print(e)
        return jsonify({"error": f'Error al editar el documento: {e}',"status": False}), 500

@app.route('/EditarDocumentPatron/<string:nombre_documento>/<string:nombre_colleccion>', methods=['PUT'])
def get_EditarPatrones(nombre_documento, nombre_colleccion):
    datos_solicitud = request.get_json()
    Definicion = datos_solicitud ['DefinicionUpdate']
    Titulo = datos_solicitud ['TituloUpdate']
    Resultados = datos_solicitud ['ResultadoUpdate']
    Alteraciones = datos_solicitud ['AlteracionesUpdate']
    Valorar = datos_solicitud ['ValorarUpdate']
    try:
        informacion_adicional_ref = db.collection('Patrones').document(nombre_documento).collection(nombre_colleccion).document("Descripcion")
        documento_actual = informacion_adicional_ref.get()
        
        if documento_actual.exists:
            informacion_adicional_ref.update({"Titulo": Titulo,"Definicion": Definicion,"Resultados":Resultados,"Alteraciones":Alteraciones,"Valoraciones":Valorar})
            documento_actualizado = informacion_adicional_ref.get().to_dict()
            print(documento_actualizado)
            return jsonify({"mensaje": f'Documento {nombre_documento} actualizado', "datos": documento_actualizado, "status": True})
        else:
            return jsonify({"mensaje": f'Documento {nombre_documento} no encontrado',"status": False}), 404

    except Exception as e:
        print(e)
        return jsonify({"error": f'Error al editar el documento: {e}',"status": False}), 500





# Ruta para actualizar un elemento por ID
@app.route('/Necesidades/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    updated_item = request.get_json()
    db.collection('Necesidades').document(item_id).update(updated_item)
    return jsonify({"message": "Necesidad actualizada correctamente"})

# Ruta para eliminar un elemento por ID
@app.route('/Necesidades/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    db.collection('Necesidades').document(item_id).delete()
    return jsonify({"message": "Necesidad eliminada correctamente"})


@app.route('/Chat/Chatbot', methods=['POST'])
def postChat():
    datos_solicitud = request.get_json()
    msj = datos_solicitud['Mensaje']
    ejm = chat.send_message("Actua como profesional enfermero y responde preguntas solo en el ambito de enfermeria,"+ 
                      "si te preguntan fuera de esa área contesta con: "+
                      "'Mi ambito de conocimiento esta basado en el ámbito de enfermeria, "+
                      "porfavor ingresa una intruccion en esa área.'")
    for chunk in ejm:
        print(chunk.text)
    response = chat.send_message(msj)
    ConjuntoDatos = ""
    for chunk in response:
        ConjuntoDatos=ConjuntoDatos + chunk.text
    return jsonify({"Respuesta": ConjuntoDatos})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)