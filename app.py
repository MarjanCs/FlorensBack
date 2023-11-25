from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore, auth

app = Flask(__name__)

# Configurar la conexión con Firebase
cred = credentials.Certificate('api/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Ruta para obtener todos los elementos
@app.route('/Necesidades', methods=['GET'])
def get_items():
    items = db.collection('Necesidades_14').stream()
    print(items)
    item_list = [item.to_dict() for item in items]
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

        # Si no se produce una excepción, el usuario existe
        
        return jsonify({"mensaje": "Usuario existe"}), 200

    except auth.AuthError as e:
        # Si hay un error de autenticación, verificar el tipo de error
        if e.detail == 'USER_NOT_FOUND':
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
        else:
            return jsonify({"mensaje": "Error de autenticación"}), 500




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
    app.run(debug=True)