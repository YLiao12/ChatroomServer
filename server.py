import mysql.connector
import json
from flask import Flask
    
app = Flask(__name__)

# mydb = mysql.connector.connect(
#   host="18.219.7.155",       # 数据库主机地址
#   user="leo",    # 数据库用户名
#   passwd="L21516114leo"   # 数据库密码
# )

@app.route("/") 
def hello_world():
    return "Hello World!"

@app.route("/api/a3/get_chatrooms")
def get_chatrooms():
    # get records from mysql
    # change records into json
    # return json
    pass

@app.route("/api/a3/get_messages")
def get_messages():
    # get chatroom_id and page from the api
    # get message from mysql
    # change into json. return
    pass

@app.route("/api/a3/send_message")
def send_message():
    # get chatroom_id, user_id, name, message from post api
    # write into mysql
    # return status OK json
    pass

if __name__ == "__main__": 
    app.run()