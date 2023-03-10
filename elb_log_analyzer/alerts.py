from requests.sessions import Session
from os.path import isfile, basename

class SlackAlert:
    def __init__(self, webhook_url: str) -> None:
        assert isinstance(webhook_url, str)

        self._session = Session()
        self._webhook_url = webhook_url


    def send_message(self, message: str):
        assert isinstance(message, str)

        payload = {
            'type':'mrkdwn',
            'text': message
        }

        res = self._session.post(url=self._webhook_url, json=payload)
        return res
