from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def healthcheck():
    return "The server is running! (Todo-api of the snake)"

# start the development server using the run() method
if __name__ == "__main__":
    app.run()