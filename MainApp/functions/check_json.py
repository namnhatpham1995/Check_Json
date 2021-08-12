# file contains code to check json request
from datetime import datetime

from flask import request
from MainApp.functions.json_functions import *
from MainApp import db
from MainApp.functions.db_functions import *
from MainApp.models import hourly_stats, ip_blacklist, ua_blacklist, customer


def check_json():
    if request.method == 'POST' and request.is_json:
        content = request.get_json()
        request_content = list(content.keys())
        json_content = ["customerID", "customerName", "request_info", "remoteIP"]
        # check if the length of JSON request match with default
        if len(request_content) != len(json_content):  # if no, ignore
            return "Malformed request, removed"
        else:  # if yes
            # check if it has enough required contents
            good_request, id_available, customer_Name, customer_ID, request_info, remote_IP = check_json_contents(request_content, content)
            if good_request == len(json_content):  # if JSON req has enough required contents
                # check IP and customer name in blacklist
                ip_bl_table = check_ip_blacklist(remote_IP)
                ua_bl_table = check_ua_blacklist(customer_Name)
                if ip_bl_table is None and ua_bl_table is None:  # if not found in blacklist
                    customer_table = check_customer_info(customer_ID)  # check customer info
                    if customer_table is not None:
                        if customer_table.name == customer_Name:  # check if customer name is provided right
                            # Check if customer is in active state
                            if customer_table.active == 1:  # customer active
                                hourly_stats_table = hourly_stats_latest(customer_ID)
                                # check if data found
                                # If no record of request or the last record was in different hour, create new record
                                if hourly_stats_table is None \
                                        or (hourly_stats_table.time.hour != datetime.now().hour):
                                    msg = hourly_stats_new(customer_ID, "good")
                                    return msg
                                else:  # if the last record was in same hour, increase invalid_count and update timestamp
                                    msg = hourly_stats_fix_data(hourly_stats_table, "good")
                                    return msg

                            else:  # customer inactive
                                return "Customer inactive, removed"
                        else:  # if customer name is provided wrong
                            # Check if customer is in active state
                            if customer_table.active == 1:  # customer active
                                # check customer request data and take the latest info
                                hourly_stats_table = hourly_stats_latest(customer_ID)
                                # check if data found
                                # If no record of request or the last record was in different hour, create new record
                                if hourly_stats_table is None \
                                        or (hourly_stats_table.time.hour != datetime.now().hour):
                                    msg = hourly_stats_new(customer_ID, "invalid")
                                    return msg
                                else:  # if the last record was in same hour, increase invalid_count and update timestamp
                                    msg = hourly_stats_fix_data(hourly_stats_table, "invalid")
                                    return msg
                            else:  # customer inactive
                                return "Customer inactive, removed"
                    else:
                        return "Invalid ID, removed"
                else:
                    return "Blacklist, removed"
            else:  # if JSON don't have enough required contents
                if id_available == 1:  # if there is an ID to check
                    # Check id and add invalid count
                    customer_table = check_customer_info(customer_ID)  # check customer info
                    if customer_table is not None:
                        # Check if customer is in active state
                        if customer_table.active == 1:  # customer active
                            # check customer request data and take the latest info
                            hourly_stats_table = hourly_stats_latest(customer_ID)
                            # check if data found
                            # If no record of request or the last record was in different hour, create new record
                            if hourly_stats_table is None \
                                    or (hourly_stats_table.time.hour != datetime.now().hour):
                                msg = hourly_stats_new(customer_ID, "invalid")
                                return msg
                            else:  # if the last record was in same hour, increase invalid_count and update timestamp
                                msg = hourly_stats_fix_data(hourly_stats_table, "invalid")
                                return msg
                        else:  # customer inactive
                            return "Customer inactive, removed"
                    else:
                        return "Invalid ID, removed"
                else:
                    return "Not enough info, removed"
    else:
        return "Please send JSONed POST request"
