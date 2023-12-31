from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin import exceptions

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
    #documentos_coleccion = db.collection('Necesidades').stream()
    #datos_coleccion = {doc.id: doc.to_dict() for doc in documentos_coleccion}

    # Presentar como JSON
    #return jsonify(datos_coleccion)


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
        'universidad': datos_user['universidad']
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
            return jsonify({"status": True,"mensaje": "Usuario existe"}), 200
        else:
            return jsonify({"status": False,"mensaje": "Contraseña Incorrecta"}), 404

    except exceptions.FirebaseError as e:
        # Si hay un error de autenticación, verificar el tipo de error
        return jsonify({"mensaje": "Usuario no encontrado","status": False,}), 404


#Ruta para la lista de documentos de necesidades
@app.route('/DocumentsNece', methods=['GET'])
def get_documentsNece():
    items = db.collection('Necesidades').stream()
    print(items)
    datos_coleccion = {}
    #nombres_documentos = [{'id': str(i+1), 'nombre': doc.id} for i, doc in enumerate(items.get())]
    #item_list = [item.to_dict() for item in items]
    for i, doc in enumerate(items):
            # Usar el índice como ID comenzando desde 1
            identificador = str(i + 1)
            datos = doc.to_dict()
            datos["Id"] = doc.id
            datos_coleccion[identificador] = datos
    return jsonify(datos_coleccion)

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


#Ruta para la lista de documentos de patrones
@app.route('/DocumentsPatro', methods=['GET'])
def get_documentspatro():
    items = db.collection('Patrones')
    print(items)
    nombres_documentos = [{'id': str(i+1), 'nombre': doc.id} for i, doc in enumerate(items.get())]
    #item_list = [item.to_dict() for item in items]
    
    return jsonify(nombres_documentos)
#Ruta para obtener una informacion Patrones
@app.route('/DocPatronesInfo', methods=['POST'])
def get_PatronesDocInfo():
    datos_solicitud = request.get_json()
    doc = datos_solicitud['Document']
    try:
        informacion_adicional_ref = db.collection('Patrones').document(doc).get().to_dict()
        return jsonify(informacion_adicional_ref)
    except Exception as e:
        return jsonify({"mensaje": "Error al obtener la Información","status": False,}), 404




# Ruta para agregar un nuevo elemento
@app.route('/Necesidades', methods=['POST'])
def add_item():
    new_item = request.get_json()
    doc_ref = db.collection('Necesidades_14').add(new_item)
    return jsonify({"id": doc_ref.id})

# Ruta para actualizar un elemento por ID
@app.route('/Necesidades/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    updated_item = request.get_json()
    db.collection('Necesidades_14').document(item_id).update(updated_item)
    return jsonify({"message": "Necesidad actualizada correctamente"})

# Ruta para eliminar un elemento por ID
@app.route('/Necesidades/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    db.collection('Necesidades_14').document(item_id).delete()
    return jsonify({"message": "Necesidad eliminada correctamente"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)