from datetime import datetime

from sqlalchemy import cast, String

from MainApp import app, db
from flask import request, render_template
from MainApp.models import customer, ip_blacklist, ua_blacklist, hourly_stats
from flask_expects_json import expects_json

'''
schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'customer_id': {'type': 'string'},
        'timestamp': {'type': 'string'},
        'request_count': {'type': 'string'},
        'invalid_count': {'type': 'string'}
    },
    'required': ['id', 'customer_id', 'timestamp', 'request_count', 'invalid_count']
}
'''
schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
    },
    'required': ['name', 'email']
}


@app.route('/check_json', methods=['POST'])
def postJsonHandler():
    if request.method == 'POST' and request.is_json:
        good_request = 0
        id_available = 0
        content = request.get_json()
        request_content = list(content.keys())
        json_content = ["customerID", "customerName", "request_info", "remoteIP"]
        # check if the length of JSON request match with default
        if len(request_content) != len(json_content):  # if no, ignore
            return "Malformed request, removed"
        else:  # if yes
            # check if it has enough required contents
            for a in range(len(request_content)):
                if request_content[a] == 'customerID':
                    customer_ID = content['customerID']
                    good_request += 1
                    id_available = 1
                elif request_content[a] == 'customerName':
                    customer_Name = content['customerName']
                    good_request += 1
                elif request_content[a] == 'request_info':
                    request_info = content['request_info']
                    good_request += 1
                elif request_content[a] == "remoteIP":
                    remote_IP = content['remoteIP']
                    good_request += 1
            if good_request == len(json_content):  # if JSON req has enough required contents
                # check IP and customer name in blacklist
                ip_bl_table = ip_blacklist.query.filter_by(ip=remote_IP).first()
                ua_bl_table = ua_blacklist.query.filter_by(ua=customer_Name).first()
                if ip_bl_table is None and ua_bl_table is None:  # if not found in blacklist
                    customer_table = customer.query.filter_by(id=customer_ID).first()  # check customer info
                    if customer_table.name == customer_Name:  # check if customer name is provided right
                        # Check if customer is in active state
                        if customer_table.active == 1:  # customer active
                            # check customer request data and take the latest info
                            hourly_stats_table = hourly_stats.query \
                                .filter_by(customer_id=customer_ID) \
                                .order_by(hourly_stats.id.desc()) \
                                .first()  # take the latest request info of customer
                            # check if data found
                            # If no record of request or the last record was in different hour, create new record
                            if hourly_stats_table is None \
                                    or (hourly_stats_table.time.hour != datetime.now().hour):
                                db.session.add(hourly_stats(customer_id=customer_ID, request_count=1,
                                                            time=datetime.now(), invalid_count=0))
                                db.session.commit()
                                return "Saved new record with good request"
                            else:  # if the last record was in same hour, increase invalid_count
                                hourly_stats_table.request_count = hourly_stats_table.request_count + 1
                                db.session.commit()
                                return "Saved additional record with good request"

                        else:  # customer inactive
                            return "Customer inactive, removed"
                    else:  # if customer name is provided wrong
                        # Check if customer is in active state
                        if customer_table.active == 1:  # customer active
                            # check customer request data and take the latest info
                            hourly_stats_table = hourly_stats.query \
                                .filter_by(customer_id=customer_ID) \
                                .order_by(hourly_stats.id.desc()) \
                                .first()  # take the latest request info of customer
                            # check if data found
                            # If no record of request or the last record was in different hour, create new record
                            if hourly_stats_table is None \
                                    or (hourly_stats_table.time.hour != datetime.now().hour):
                                db.session.add(
                                    hourly_stats(customer_id=customer_ID, request_count=0, time=datetime.now(),
                                                 invalid_count=1))
                                db.session.commit()
                                return "Saved new record with invalid request (wrong name)"
                            else:  # if the last record was in same hour, increase invalid_count
                                hourly_stats_table.invalid_count = hourly_stats_table.invalid_count + 1
                                db.session.commit()
                                return "Saved additional with invalid request (wrong name)"
                        else:  # customer inactive
                            return "Customer inactive, removed"

                else:
                    return "Blacklist, removed"
            else:  # if JSON don't have enough required contents
                if id_available == 1:  # if there is an ID to check
                    # Check id and add invalid count
                    customer_table = customer.query.filter_by(id=customer_ID).first()  # check customer info
                    # Check if customer is in active state
                    if customer_table.active == 1:  # customer active
                        # check customer request data and take the latest info
                        hourly_stats_table = hourly_stats.query \
                            .filter_by(customer_id=customer_ID) \
                            .order_by(hourly_stats.id.desc()) \
                            .first()  # take the latest request info of customer
                        # check if data found
                        # If no record of request or the last record was in different hour, create new record
                        if hourly_stats_table is None \
                                or (hourly_stats_table.time.hour != datetime.now().hour):
                            db.session.add(hourly_stats(customer_id=customer_ID, request_count=0,
                                                        time=datetime.now(), invalid_count=1))
                            db.session.commit()
                            return "Saved new record with invalid request"
                        else:  # if the last record was in same hour, increase invalid_count
                            hourly_stats_table.invalid_count = hourly_stats_table.invalid_count + 1
                            db.session.commit()
                            return "Saved additional with invalid request"
                    else:  # customer inactive
                        return "Customer inactive, removed"
                else:
                    return "Not enough info, removed"
    else:
        return "Please send JSONed POST request"


@app.route('/')
@app.route('/index')
def index():
    return render_template("base.html")
