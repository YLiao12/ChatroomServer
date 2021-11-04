from flask.wrappers import Request
import mysql.connector
from flask import Flask, request, jsonify, json
    
app = Flask(__name__)

conn = mysql.connector.connect(
  host="localhost",       # 数据库主机地址
  user="dbuser",    # 数据库用户名
  passwd="password",   # 数据库密码
  database = "iems5722",
)
cursor = conn.cursor(dictionary = True)

@app.route("/") 
def hello_world():
    return "Hello World!"

@app.route("/api/a3/get_chatrooms")
def get_chatrooms():
    # get records from mysql
    # change records into json
    # return json
    query_chatroom = "SELECT * FROM chatrooms ORDER BY id ASC"
    cursor.execute(query_chatroom)
    results = cursor.fetchall()
    jsonResult = json.dumps(results)
    # some issues about json 
    return jsonify(status="OK", data=jsonResult)
    # return jsonResult

@app.route("/api/a3/get_messages", methods=["GET"])
def get_messages():
    # get chatroom_id and page from the api
    # get message from mysql
    # change into json. return\
    chatroom_id = request.args.get("chatroom_id")
    page = request.args.get("page")
    queryMessages = "select * from messages where chatroom_id = %s"
    param = (chatroom_id, )
    cursor.execute(queryMessages, param)
    results = cursor.fetchall()
    return json.dumps(results)
    pass

@app.route("/api/a3/send_message", methods=["POST"])
def send_message():
    # get chatroom_id, user_id, name, message from post api
    # write into mysql
    # return status OK json
    chatroom_id = request.form.get("chatroom_id")
    user_id = request.form.get("user_id")
    name = request.form.get("name")
    message = request.form.get("message")

    querySendMessage = "insert into messages(chatroom_id, user_id, name, message) values (%s, %s, %s, %s);"
    param = (chatroom_id, user_id, name, message)
    cursor.execute(querySendMessage, param)
    conn.commit()
    return jsonify(status="OK")
    pass

if __name__ == "__main__": 
    app.run()