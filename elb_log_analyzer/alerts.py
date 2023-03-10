from requests.sessions import Session
from os.path import isfile


import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')

class SlackAlert:
    def __init__(self, webhook_url: str) -> None:
        assert isinstance(webhook_url, str)

        self._session = Session()
        self._webhook_url = webhook_url

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
    
        # get clients with high requests count 
        clients_data = []
        # for 
        


    def _send_message(self, message: str):
        assert isinstance(message, str)

        payload = {
            'type':'mrkdwn',
            'text': message
        }

        res = self._session.post(url=self._webhook_url, json=payload)
        return res
    
    def generate_alert(self, analyzed_log_file_location:str) -> dict:
        assert isinstance(analyzed_log_file_location, str)

        msg = self._generate_alert_message(analyzed_log_file_location)
        res = self._send_message(msg)

        return {
            'status_code': res.status_code,
            'text': res.text
        }

