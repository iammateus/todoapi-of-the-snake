from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pprint import pprint
import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:docker@mongo:27017/todos?authSource=admin"
mongo = PyMongo(app)

@app.route("/healthcheck")
def healthcheck():
    data = {'message': 'The server is running! (Todo-api of the snake)'}
    return jsonify(data)

@app.route("/todo", methods=['POST'])
def create():
    data = request.get_json()

    requiredFields = [ 'name', 'description' ]

    for field in requiredFields:
        if field not in data:
            return jsonify({
                'message': 'The ' + field + ' field is required.'
            })
    
    task = {
        "name": data['name'],
        "description": data['description'],
        "createdAt": datetime.datetime.now()
    }

    mongo.db.todos.insert_one(task)

    return jsonify({
        "message": "CREATED",
        "data": {
            "id": str(task['_id'])
        }
    }), 201

@app.route("/todo/<id>", methods=['PUT'])
def update(id):
    task = mongo.db.todos.find_one({'_id': ObjectId(id)})

    if task == None:
        return jsonify({
            "error": "The todo was not found.",
        }), 422
    
    data = request.get_json()

    requiredFields = [ 'name', 'description' ]

    for field in requiredFields:
        if field in data:
            task[field] = data[field]

    task['updatedAt'] = datetime.datetime.now()
    
    mongo.db.todos.update_one(
        {
            '_id': ObjectId(id)
        },
        {
            "$set": task
        }
    )
    
    return jsonify({
        "message": "UPDATED",
    }), 200

@app.route("/todo/<id>", methods=['DELETE'])
def delete(id):
    task = mongo.db.todos.find_one({'_id': ObjectId(id)})

    if task == None:
        return jsonify({
            "error": "The todo was not found.",
        }), 422

    mongo.db.todos.delete_one({
         '_id': ObjectId(id)
    })
    
    return jsonify({
        "message": "DELETED"
    }), 200

@app.route("/todo/<id>", methods=['GET'])
def show(id):
    task = mongo.db.todos.find_one({'_id': ObjectId(id)})

    if task == None:
        return jsonify({
            "error": "The todo was not found.",
        }), 422

    task["_id"] = str(task["_id"])
    
    return jsonify({
        "message": "SUCCESS",
        "data": task
    }), 200

@app.route("/todo", methods=['GET'])
def list():

    page = 1
    limit = 10

    if request.args.get('page') != None:
        page = int(request.args.get('page'))
    
    if request.args.get('limit') != None:
        if int(request.args.get('limit')) < 21:
            limit = int(request.args.get('limit'))

    skip = (page - 1) * limit
    tasks = mongo.db.todos.find({}).skip(skip).limit(limit)

    json_tasks = []

    for task in tasks:
        task['_id'] = str(task['_id'])
        json_tasks.append(task)
    
    return jsonify({
        "message": "SUCCESS",
        "data": json_tasks,
        "count": len(json_tasks),
        "page": page
    }), 200

# start the development server using the run() method
if __name__ == "__main__":
    app.run()
    