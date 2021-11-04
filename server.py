import mysql.connector
from flask import Flask
    
app = Flask(__name__)

@app.route("/") 
def hello_world():
    return "Hello World!"

@app.route("/api/a3/get_chatrooms")
def get_chatrooms():


if __name__ == "__main__": 
    app.run()