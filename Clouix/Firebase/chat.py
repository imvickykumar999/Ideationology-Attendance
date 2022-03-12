
from firebase_admin import db
from firebase_admin import credentials
import os

path = './Clouix/Firebase'
file = 'ideationology-4c639-firebase-adminsdk-5hfwu-5806b97f02.json'
dir = os.path.join(path, file)

cred = credentials.Certificate(dir)
url = 'https://ideationology-4c639-default-rtdb.asia-southeast1.firebasedatabase.app/'
path = {'databaseURL' : url}

import firebase_admin
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, path)


def send_mess(user, send):
    import datetime

    dt = datetime.datetime.now()
    dt += datetime.timedelta(days = 0, hours = 5, minutes = 30)

    d = str(dt).split()[0]
    t = str(dt).split()[1].split('.')[0]

    child = f"Group Chat/Message/{d}/{t}/{user}"
    db.reference(child).set(send)

def get_mess():
    child = f"Group Chat/Message"
    ref = db.reference(child).get()
    return ref
