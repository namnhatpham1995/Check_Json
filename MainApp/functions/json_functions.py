def check_json_contents(request_content, content):
    good_request = 0
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
            return good_request, id_available, customer_Name, customer_ID, request_info, remote_IP
