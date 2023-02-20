def get_client_requests_count(analyzed_data:dict):
    requests_count = {}

    for client_ip in analyzed_data.keys():
        if client_ip == 'total':
            continue
        requests_count[client_ip] = analyzed_data[client_ip]['total']

    return requests_count

def get_data(data:dict):
    return dict((k,v) for k,v in data.items() if k!='total')