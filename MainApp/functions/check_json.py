from flask import request
from MainApp.functions.json_functions import *
from MainApp.functions.db_functions import *


def check_json():
    if request.method == 'POST' and request.is_json:
        content = request.get_json()
        request_content = list(content.keys())
        json_content = ["customerID", "customerName", "request_info", "remoteIP"]
        customer_ID, customer_Name = check_json_id_name(request_content, content)
        if customer_ID is not None and customer_Name is not None:
            customer_table = check_customer_info(customer_ID)
            ua_bl_table = check_ua_blacklist(customer_Name)
            if ua_bl_table is None:
                if customer_table.name == customer_Name:
                    # Check active state of customer
                    if customer_table.active == 1:
                        # Check the num of field in request and default format
                        # If match num of field, check the remain field
                        if len(request_content) == len(json_content):
                            # Check request message and IP
                            request_info, remote_IP = check_json_remain_fields(request_content, content)
                            # Check if remaining required fields found
                            # If yes, check IP
                            if request_info is not None and remote_IP is not None:
                                ip_bl_table = check_ip_blacklist(remote_IP)
                                if ip_bl_table is None:
                                    msg = check_hourly_data(customer_ID, "good")
                                    return msg
                                else:
                                    msg = check_hourly_data(customer_ID, "invalid")
                                    return msg
                            else:
                                # check if hourly data found
                                msg = check_hourly_data(customer_ID, "invalid")
                                return msg
                        # If num of field doesn't match
                        else:
                            # check if hourly data found
                            msg = check_hourly_data(customer_ID, "invalid")
                            return msg
                    else:
                        return "Inactive customer, removed request"
                else:
                    return "Name does not match ID, removed"
            else:
                return "Blacklist User Agent, removed"
        else:
            return "No ID or Name to check identity, removed"
    else:
        return "Please send JSONed POST request"


def check_hourly_data(customer_ID, status):
    # check if hourly data found
    hourly_stats_table = hourly_stats_latest(customer_ID)
    # If no record of request or the last record was in different hour, create new record
    # with increasing invalid count
    if hourly_stats_table is None \
            or (hourly_stats_table.time.hour != datetime.now().hour):
        if status == "good":
            msg = hourly_stats_new(customer_ID, "good")
        else:
            msg = hourly_stats_new(customer_ID, "invalid")
    # if the last record was in same hour, increase invalid_count and update timestamp
    else:
        if status == "good":
            msg = hourly_stats_fix_data(hourly_stats_table, "good")
        else:
            msg = hourly_stats_fix_data(hourly_stats_table, "invalid")
    return msg
