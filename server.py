from flask import Flask, jsonify

from char_img import *
from model import *

app = Flask(__name__)

# Define an endpoint for the root URL
@app.route('/')
def home():
    return 'Welcome to the Flask App!'

# Define an endpoint for /hello
@app.route('/hello')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True, port=4000)
