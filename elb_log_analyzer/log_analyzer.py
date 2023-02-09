from re import findall

from .utils import get_abusive_ip_data, get_logs


class LogAnalyzer:
    def __init__(self, log_file_path: str, ipabuse_api_key: str=None, request_threshold: int = 150) -> None:
        assert isinstance(log_file_path, str)
        assert isinstance(request_threshold, int)

        self._ipabuse_api_key = ipabuse_api_key
        self._request_threshold = request_threshold
        self._log_lines = get_logs(log_file_path)

        # create empty list for storing logs
        self.logs: list = []
        self._log_lines_to_dict()

        # unique ips
        self.unique_ips = None

        # analyzed logs
        self.analyzed_logs = self.analyze_logs()


    def _log_lines_to_dict(self):
        '''
        description: converts log into a list of dictionary with keys (timestamp,
        elb, client, backend, request_processing_time, backend_processing_time, 
        response_processing_time, elb_status_code, backend_status_code, 
        received_bytes, sent_bytes, request, user_agent, ssl_cipher,ssl_protocol).

        '''
        for log_line in self._log_lines:
            # if log line is empty then continue
            if not log_line:
                continue

            # convert log lines into data structure
            data_between_quotes = findall('"([^"]*)"', log_line)
            request = data_between_quotes[0]
            user_agent = data_between_quotes[1]

            # remove http request and user agent from log line
            log_line = log_line.replace('h2 ', '').replace('https ', '').replace(
                'http ', '').replace(f'"{request}"', '').replace(f'"{user_agent}"', '')

            # format request into http request
            request = request.split(' ')
            http_request = {
                'method': request[0],
                'url': request[1],
                'version': request[2]
            }

            # separate log line
            log_line = log_line.split(' ')

            # separate client ip and port
            client_ip, client_port = log_line[2].split(':')
            self.logs.append({
                'timestamp': log_line[0],
                'elb': log_line[1],
                'client_ip': client_ip,
                'client_port': int(client_port),
                'backend': log_line[3],
                'request_processing_time': log_line[4],
                'backend_processing_time': log_line[5],
                'response_processing_time': log_line[6],
                'elb_status_code': log_line[7],
                'backend_status_code': log_line[8],
                'received_bytes': log_line[9],
                'sent_bytes': log_line[10],
                'request': http_request,
                'user_agent': user_agent,
                'ssl_cipher': log_line[13],
                'ssl_protocol': log_line[14]
            })

    def get_unique_ips(self):
        '''
        description: returns lis of unique ip addresses from logs
        returns: list
        '''
        if len(self.logs) == 0:
            self._log_lines_to_dict()

        # extract unique ips
        ips = []
        for log in self.logs:
            ip = log.get('client_ip', "127.127.127.127")
            if ip not in ips:
                ips.append(ip)

        self.unique_ips = ips

        return ips

    def count_request_by_client_ip(self):
        '''
        description: get requests count by client ip.
        returns: dict {'ip': count}
        '''
        # get unique ips if not analyzed
        if not self.unique_ips:
            self.unique_ips = self.get_unique_ips()

        # create list of requests count by client ip
        request_counts = {client_ip: 0 for client_ip in self.unique_ips}

        # count request by each ip
        for ip in self.unique_ips:
            for log in self.logs:
                if ip == log['client_ip']:
                    request_counts[ip] += 1
        
        # convert it to list
        return request_counts

    def analyze_logs(self):
        '''
        description: analyze logs line by line and returns data in below format.

        {
            'total': count(int),
            'ip': {
                'total': count(int),
                'ports':[] (list(int)),
                'user_agents': [] (list(str)),
                'ip_abuse_data': None,
                'requests':{
                    'HTTP_METHOD': {'url' : {'count' :int, 'elb_status_codes':[], 'backend_status_codes':[]} , 'total':count(int)},
                }
            }
        }

        returns: dict
        '''
        data = {'total': 0}
        for log in self.logs:
            # increment total request count
            data['total'] += 1

            # start analyzing client request
            client = log.get('client_ip')

            if client not in data.keys():
                data[client] = {
                    'total': 0,
                    'ports': [],
                    'user_agents': [],
                    'requests': {
                    }
                }

            # update total count value
            data[client]['total'] += 1

            # update ports
            if log['client_port'] not in data[client]['ports']:
                data[client]['ports'].append(log['client_port'])

            # update user agent (can be used to detect anomaly)
            if log['user_agent'] not in data[client]['user_agents']:
                data[client]['user_agents'].append(log['user_agent'])

            # Count urls hits
            # if HTTP method is not present then create in dict
            if log['request']['method'] not in data[client]['requests'].keys():
                data[client]['requests'][log['request']
                                         ['method']] = {'total': 0}
            # increment total count
            data[client]['requests'][log['request']['method']]['total'] += 1

            # if URL is not present in requests then create one
            if log['request']['url'] not in data[client]['requests'].keys():
                data[client]['requests'][log['request']['method']].update({log['request']['url']: {
                                                                          'count': 0, 'elb_status_codes': [], 'backend_status_codes': [], 'timestamps': []}})

            # update url hit count, status code and time stamps
            data[client]['requests'][log['request']['method']
                                     ][log['request']['url']]['count'] += 1
            data[client]['requests'][log['request']['method']][log['request']
                                                               ['url']]['elb_status_codes'].append(log['elb_status_code'])
            data[client]['requests'][log['request']['method']][log['request']
                                                               ['url']]['backend_status_codes'].append(log['backend_status_code'])
            data[client]['requests'][log['request']['method']
                                     ][log['request']['url']]['timestamps'].append(log['timestamp'])
        
        # get abuse details if threshold increases
        if self._ipabuse_api_key:
            for client_ip in data.keys():
                if client_ip == 'total':
                    continue

                if data[client_ip]['total'] > self._request_threshold:
                    ipabuse_data = get_abusive_ip_data(client_ip, self._ipabuse_api_key)
                    data[client_ip]['ip_abuse_data'] = ipabuse_data

        return data
