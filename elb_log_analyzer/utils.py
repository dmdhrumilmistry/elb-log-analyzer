from requests import get as r_get
from requests.models import Response
from json import JSONDecodeError
from os.path import isfile


def get_abusive_ip_data(ip: str, api_key: str):
    '''
    description: get abusive ip details
    returns: dict
    '''
    assert isinstance(ip, str)
    assert isinstance(api_key, str)

    headers = {
        'Key': api_key,
        'Accept': 'application/json',
    }
    params = {
        'ipAddress': ip,
        'maxAgeInDays': 90
    }

    res:Response = r_get(
        'https://api.abuseipdb.com/api/v2/check',
        params=params,
        headers=headers
    )
    
    try:
        data = res.json()
    except JSONDecodeError:
        data = {'msg': f'Error while fetching ip details of {ip}'}
    return data


def get_logs(file_path:str):
    '''
    description: extract logs from a file and returns log lines as string.
    returns: list[str] or None
    '''
    assert isinstance(file_path, str)

    # if file is not present return None
    if not isfile(file_path):
        raise FileNotFoundError(f'{file_path} file not found.')
    
    with open(file_path, 'r') as f:
        log_lines = f.readlines()

    return log_lines
