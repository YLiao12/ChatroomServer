from flask.wrappers import Request
import mysql.connector
from flask import Flask, request, jsonify, json
from celery import Celery
from task import send_push

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)

conn = mysql.connector.connect(
  host="localhost",       
  user="leo",    
  passwd="L21516114leo",   
  database = "iems5722",
)
cursor = conn.cursor(dictionary = True)

app.config.update(
    CELERY_BROKER_URL='amqp://guest@localhost//',
    # CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = make_celery(app)

@app.route("/") 
def hello_world():
    return "Hello World!"

@app.route("/api/a3/get_chatrooms")
def get_chatrooms():
    # get records from mysql
    # change records into json
    # return json
    query_chatroom = "SELECT * FROM chatrooms ORDER BY id ASC"
    while True:
        try:
            cursor.execute(query_chatroom)
            break
        except Exception:
            conn.ping(True)
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
    while True:
        try:
            cursor.execute(queryMessages, param)
            break
        except Exception:
            conn.ping(True)
    all_results = cursor.fetchall()
    current_msg_num = len(all_results)
    current_msg_id = int(all_results[len(all_results) - 1]["id"])
    # print(current_msg_id)
    # 
    # select page using current_msg_id (every page 10 messages)
    # delete key "id" and "chatroom_id" in every dict selected in results list
    if current_msg_num % 10:
        total_pages = int(current_msg_num / 10) + 1
    else:
        total_pages = int(current_msg_num /10)
    print(current_msg_num)
    print(total_pages)
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
    
    query_messages_page = "select * from messages where chatroom_id = %s and id <= %s and id >= %s order by id DESC"
    param_page = (chatroom_id, endingId, startingId)
    cursor.execute(query_messages_page, param_page)
    
    results = cursor.fetchall()
    new_result = []
    for result in results:
        del result["id"]
        del result["chatroom_id"]
        new_result.append(result)
    # new_result.reverse()
    messages_list_json = json.dumps(new_result)
    data_json = jsonify(current_page = page, messages=messages_list_json, total_pages = total_pages)
    # data = json.loads(str(data_json)) 
    data = data_json.get_json()
    result_json = jsonify(data=data, status="OK")
    return result_json

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
    while True:
        try:
            cursor.execute(querySendMessage, param)
            conn.commit()
            break
        except Exception:
            conn.ping(True)
    
    send_push.delay(name, message)
    return jsonify(status="OK")
    # pass
    

@app.route("/api/a4/submit_push_token", methods=["POST"])
def submit_push_token():
    user_id = request.form.get("user_id")
    token = request.form.get("token")
    querySendMessage = "insert into push_tokens(user_id, token) values (%s, %s);"
    param = ( user_id, token)
    while True:
        try:
            cursor.execute(querySendMessage, param)
            conn.commit()
            break
        except Exception:
            conn.ping(True)
    return jsonify(status="OK")


if __name__ == "__main__": 
    app.run(debug = True, host = '0.0.0.0', port='8080')
