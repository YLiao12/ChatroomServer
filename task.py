from celery import Celery
from flask import Flask
from pyfcm import FCMNotification
import mysql.connector


app = Flask(__name__)

conn = mysql.connector.connect(
  host="localhost",       
  user="leo",    
  passwd="L21516114leo",   
  database = "iems5722",
)
cursor = conn.cursor(dictionary = True)

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

app.config.update(
    CELERY_BROKER_URL='amqp://guest@localhost//',
)

celery = make_celery(app)

@celery.task()
def send_push(name, message):
    push_service = FCMNotification(api_key = "AAAAViDzwi0:APA91bHFScstMcDN3e7lmUxcgr4OrDHAmcmI2dVsZkOS9QAVpdXlsUQjhoIYsS8Lj7pU2rQ9XEXCpnZmHcPZVEHN5ghOc7jYKnJdce6giENsKcj4UHlxL8pIkXpxQlkpiR-vxJJR5gcH")
    registration_id = "cHqVYDwWQ0i5tv4Lpld8iF:APA91bGm1vdTDPCklg4Au4l3nLs22GGQfwbkLtqYEDf1U_CffdNXpj7_j7ti4vXzmlO-l8Bxqi5xzYIJVUkKYO64kIzscHZhinjVBqwGD1CgIqWEHzFGO1CKDs9B9m5KWWFOrrdl-nX-"
    
    queryMessages = "select token from messages where user_id = %s"
    param = ("1155161159", )
    while True:
        try:
            cursor.execute(queryMessages, param)
            break
        except Exception:
            conn.ping(True)
    results = cursor.fetchall()
    print(results)
    message_title = name
    message_body = message
    # result = push_service.notify_single_device(
    #     registration_id = registration_id,
    #     message_title = message_title,
    #     message_body = message_body)
    result = push_service.notify_multiple_devices(
        registration_ids=results,
        message_title = message_title,
        message_body = message_body
    )
