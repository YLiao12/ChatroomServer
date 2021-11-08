from flask.wrappers import Request
import mysql.connector
from flask import Flask, request, jsonify, json
    
app = Flask(__name__)

conn = mysql.connector.connect(
  host="localhost",       
  user="leo",    
  passwd="L21516114leo",   
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
    page = int(request.args.get("page"))
    queryMessages = "select * from messages where chatroom_id = %s"
    param = (chatroom_id, )
    cursor.execute(queryMessages, param)
    all_results = cursor.fetchall()
    current_msg_id = int(all_results[len(all_results) - 1]["id"])
    print(current_msg_id)
    # 
    # select page using current_msg_id (every page 10 messages)
    # delete key "id" and "chatroom_id" in every dict selected in results list

    total_pages = current_msg_id / 10 + 1
    if page > total_pages:
        return jsonify(message="You are requesting more than total page ", status = "ERROR")

    showing_messages = None
    # calculating starting id and ending id
    # for i in range ( , )
    if page == 1:
        startingId = (total_pages - page) * 10 + 1
        endingId = current_msg_id
    else:
        startingId = (total_pages - page) * 10 + 1
        endingId = startingId + 9
    
    query_messages_page = "select * from messages where chatroom_id = %s and id <= %s and id >= %s"
    param_page = (chatroom_id, endingId, startingId)
    cursor.execute(query_messages_page, param_page)
    
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

    if chatroom_id == None or user_id == None or  name == None or message == None:
        return jsonify(message="Send parameters should not be None! ", status = "ERROR")

    querySendMessage = "insert into messages(chatroom_id, user_id, name, message) values (%s, %s, %s, %s);"
    param = (chatroom_id, user_id, name, message)
    cursor.execute(querySendMessage, param)
    conn.commit()
    return jsonify(status="OK")
    pass

if __name__ == "__main__": 
    app.run(debug = True, host = '0.0.0.0', port='8080')