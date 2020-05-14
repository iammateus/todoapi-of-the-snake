from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
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
    })

# start the development server using the run() method
if __name__ == "__main__":
    app.run()
    