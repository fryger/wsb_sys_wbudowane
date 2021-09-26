from tinydb import TinyDB
from ocv import *
from mailer import *



db = TinyDB('./db.json')


def calculate_spots():
    table = db.table('Task')   
    task = table.all()[0]
    value = int(task['spots']) - calculateSpots(int(task['width']),int(task['height']), int(task['top']), int(task['left']),task['url'])
    send_email(task['name'], value)



    
