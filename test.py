from flask.wrappers import Request
import mysql.connector
from flask import Flask

conn = mysql.connector.connect(
  host="localhost",
  user="leo",
  passwd="L21516114leo",
  database = "iems5722",
)

app = Flask(__name__)

cursor = conn.cursor(dictionary = True)

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/test")
def test():
    conn.close()
    query_chatroom = "SELECT * FROM chatrooms ORDER BY id ASC"
    while True:
        try:
            cursor.execute(query_chatroom)
            return "hello reconnect"
            break
        except Exception:
            conn.ping(True)

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port='8080')

