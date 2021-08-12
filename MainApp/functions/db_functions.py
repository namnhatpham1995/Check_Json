from datetime import datetime

from MainApp import db
from MainApp.models import hourly_stats, ip_blacklist, ua_blacklist, customer


def check_customer_info(customer_ID):
    customer_table = customer.query.filter_by(id=customer_ID).first()
    return customer_table


def check_ua_blacklist(customer_Name):
    ua_bl_table = ua_blacklist.query.filter_by(ua=customer_Name).first()
    return ua_bl_table


def check_ip_blacklist(remote_IP):
    ip_bl_table = ip_blacklist.query.filter_by(ip=remote_IP).first()
    return ip_bl_table


def hourly_stats_latest(customer_ID):
    # check customer request data and take the latest info
    hourly_stats_table = hourly_stats.query \
        .filter_by(customer_id=customer_ID) \
        .order_by(hourly_stats.id.desc()) \
        .first()  # take the latest request info of customer
    return hourly_stats_table


def hourly_stats_new(customer_ID, status):
    if status == "good":
        db.session.add(hourly_stats(customer_id=customer_ID, request_count=1,
                                    time=datetime.now(), invalid_count=0))
        db.session.commit()
        return "Saved new record with good request"
    else:
        db.session.add(hourly_stats(customer_id=customer_ID, request_count=0,
                                    time=datetime.now(), invalid_count=1))
        db.session.commit()
        return "Saved new record with invalid request"


def hourly_stats_fix_data(hourly_stats_table, status):
    if status == "good":
        hourly_stats_table.request_count = hourly_stats_table.request_count + 1
        hourly_stats_table.time = datetime.now()
        db.session.commit()
        return "Fix table with increase request count"
    else:
        hourly_stats_table.request_count = hourly_stats_table.request_count + 1
        hourly_stats_table.invalid_count = hourly_stats_table.invalid_count + 1
        hourly_stats_table.time = datetime.now()
        db.session.commit()
        return "Fix table with increase invalid request and request count"
