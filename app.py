from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/healthcheck")
def healthcheck():
    data = {'message': 'The server is running! (Todo-api of the snake)'}
    return jsonify(data)

# start the development server using the run() method
if __name__ == "__main__":
    app.run()