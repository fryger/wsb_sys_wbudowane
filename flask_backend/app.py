# import main Flask class and request object
import re
from flask import Flask, request
from flask import jsonify
from flask import Response
from flask_cors import CORS
from ocv import *
from tinydb import TinyDB, Query
from apscheduler.schedulers.background import BackgroundScheduler
from mailer import *
from schedul import *

# create the Flask app
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})
sched = BackgroundScheduler(daemon=True)

db = TinyDB('./db.json')


@app.route('/email', methods=['GET'])
def get_email_config(): 
    table = db.table('Email')   
    config = table.all()[0]
    sender = config['sender']
    receiver = config['receiver']

    return jsonify(sender=sender, receiver=receiver)

@app.route('/email', methods=['POST'])
def set_email_config():
    
    request_data = request.get_json()
    if 'sender' in request_data:
        table.update({'sender': request_data['sender']})
    if 'password' in request_data:
        table.update({'pass': request_data['password']})
    if 'receiver' in request_data:
        table.update({'receiver': request_data['receiver']})

    return Response()

@app.route('/', methods=['GET'])
def get_spot_config():
    table = db.table('Task')   
    task = table.all()[0]

    return jsonify(
        name=task['name'],
        urls=task['url'],
        spots=task['spots'],
        time=task['time'],
        width=task['width'],
        height=task['height'],
        left=task['left'],
        top=task['top'],
    )


@app.route('/', methods=['POST'])
def set_spot_config():
    table = db.table('Task')   
    

    request_data = request.get_json()

    table.update({'name': request_data['name']})
    table.update({'width': request_data['width']})
    table.update({'height': request_data['height']})
    table.update({'left': request_data['left']})
    table.update({'top': request_data['top']})
    table.update({'spots': request_data['spots']})
    table.update({'url': request_data['url']})
    scheduleTime = request_data['time']
    table.update({'time': scheduleTime})
    
   
    # sched.add_job(calculate_spots,'interval',minutes=3)
    sched.remove_all_jobs()
    sched.add_job(calculate_spots,'cron',hour=scheduleTime.split(':')[0], minute=scheduleTime.split(':')[1], id='spot_job')
    try:
        sched.start()
    except:
        pass

    return Response()

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
