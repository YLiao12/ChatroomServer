import mysql.connector
from flask import Flask
    
app = Flask(__name__)

mydb = mysql.connector.connect(
  host="18.219.7.155",       # 数据库主机地址
  user="leo",    # 数据库用户名
  passwd="L21516114leo"   # 数据库密码
)

@app.route("/") 
def hello_world():
    return "Hello World!"

@app.route("/api/a3/get_chatrooms")
def get_chatrooms():
    pass

if __name__ == "__main__": 
    app.run()