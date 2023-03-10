from requests.sessions import Session
from os.path import isfile
from json import loads as json_loads


import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')

class SlackAlert:
    def __init__(self, webhook_url: str) -> None:
        assert isinstance(webhook_url, str)

        self._session = Session()
        self._webhook_url = webhook_url

    def __get_request_with_ipabuse_data(self, data:dict):
        '''
        to be used inside _generate_alert_message 
        for extracting details of clients with ip
        abusive data.
        '''
        # get clients with high requests count
        high_req_clients_data = []
        for client_ip in data.keys():
            if client_ip == 'total':
                continue
            
            # get abusive ip data
            if data[client_ip].get('ip_abuse_data', None):
                ip_abuse_data = data[client_ip]['ip_abuse_data']
                ip_abuse_data['total_requests'] = data[client_ip]['total']
                high_req_clients_data.append(ip_abuse_data)

        return high_req_clients_data


    def _generate_alert_message(self, analyzed_log_file_location:str):
        '''
        generates alert message from analyzed log file.
        sends alert message with ips having request rate greater than
        threshold value along with their ip details.
        '''
        assert isinstance(analyzed_log_file_location, str)
        
        # return error if log file is not present
        if not isfile(analyzed_log_file_location):
            msg = f'Analyzed File Not found at {analyzed_log_file_location}'
            logger.error(msg)
            return ':open_file_folder: ' + msg
    
        # read data from file
        data = None
        with open(analyzed_log_file_location, 'r') as f:
            data = json_loads(f.read())

        abusive_client_details = self.__get_request_with_ipabuse_data(data)
        
        # create message from data
        msg = ':alert: _Abusive Client Details_ \n\n'
        msg = f'Analyzed Log File Location: {analyzed_log_file_location}\n\n'

        for client in abusive_client_details:
            for k,v in client.items():
                msg += f'{k}:\t{v}\n'
            msg += '='*8
            msg += '\n\n'

        return msg

    def _send_message(self, message: str):
        assert isinstance(message, str)

        payload = {
            'type':'mrkdwn',
            'text': message
        }

        res = self._session.post(url=self._webhook_url, json=payload)
        return res
    
    def generate_alert(self, analyzed_log_file_location:str):
        assert isinstance(analyzed_log_file_location, str)

        msg = self._generate_alert_message(analyzed_log_file_location)
        res = self._send_message(msg)

        return {
            'status_code': res.status_code,
            'text': res.text
        }
