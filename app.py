from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Inicializa la aplicación de Firebase con las credenciales
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sensormonitor-87c22-default-rtdb.firebaseio.com'
})

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    ref = db.reference('/data')
    new_ref = ref.push(data)
    return jsonify({'id': new_ref.key}), 201

@app.route('/get_data/<string:data_id>', methods=['GET'])
def get_data(data_id):
    ref = db.reference(f'/data/{data_id}')
    data = ref.get()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Data not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
