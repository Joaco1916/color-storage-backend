from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/colorstoragedb'
mongo = PyMongo(app)

CORS(app)

db_users = mongo.db.users
db_colors = mongo.db.colors

@app.route('/')
def index():
    return '<h1>Hello world</h1>'

# User
@app.route('/users', methods=['POST'])
def createUser():
    result = db_users.insert_one({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    return jsonify(str(ObjectId(result.inserted_id)))

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db_users.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify({users})

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = db_users.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password'],
    })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    db_users.delete_one({'_id': ObjectId(id)})
    return jsonify({
        'msg': 'Usuario eliminado exitosamente'
    })

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    db_users.update_one({'_id': ObjectId(id)}, {
        '$set':{
            'name': request.json['name'],
            'email': request.json['email'],
            'password': request.json['password']
        }
    })
    return jsonify({'msg': 'Usuario actualizado exitosamente'})

# Color
@app.route('/colors', methods=['POST'])
def createColor():
    result = db_colors.insert_one({
        'label': request.json['label'],
        'key': request.json['key'],
        'hexacode': request.json['hexacode']
    })
    return jsonify(str(ObjectId(result.inserted_id)))

@app.route('/colors', methods=['GET'])
def getColors():
    colors = []
    for doc in db_colors.find():
        colors.append({
            '_id': str(ObjectId(doc['_id'])),
            'label': doc['label'],
            'key': doc['key'],
            'hexacode': doc['hexacode']
        })
    return jsonify(colors)

@app.route('/colors/<hexa>', methods=['GET'])
def getColor(hexa):
    color = db_colors.find_one({'hexacode': ObjectId(hexa)})
    return jsonify({
        '_id': str(ObjectId(color['_id'])),
        'label': color['label'],
        'key': color['key'],
        'hexacode': color['hexacode'],
    })

@app.route('/colors/<id>', methods=['DELETE'])
def deleteColor(id):
    db_colors.delete_one({'_id': ObjectId(id)})
    return jsonify({
        'msg': 'Color eliminado exitosamente'
    })

@app.route('/colors/<id>', methods=['PUT'])
def updateColor(id):
    db_colors.update_one({'_id': ObjectId(id)}, {
        '$set':{
            'label': request.json['label'],
            'key': request.json['key'],
            'hexacode': request.json['hexacode']
        }
    })
    return jsonify({
        'msg': 'Color actualizado exitosamente'
    })

if __name__ == "__main__":
    app.run(debug=True)