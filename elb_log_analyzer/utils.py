from requests import get as r_get
from requests.models import Response
from json import JSONDecodeError
from os import listdir
from os.path import isfile, isdir, join as path_join


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
        data = res.json().get("data", None)
    except JSONDecodeError:
        data = {'msg': f'Error while fetching ip details of {ip}'}
    return data

def read_file_lines(file_path:str):
    '''
    description: takes file path and returns lines as list
    returns: list 
    '''
    assert isinstance(file_path, str)

    log_lines = []
    if isfile(file_path):
        with open(file_path, 'r') as f:
            log_lines = f.readlines()

    return log_lines
        


def get_logs(path:str):
    '''
    description: extract logs from a file and returns log lines as string.
    returns: list[str] or None
    '''
    assert isinstance(path, str)

    log_lines = []
    # if path is a directory then combine log lines from .log files inside the directory 
    if isdir(path):
        # TODO: add logic to extract log lines from log files stored in directory
        log_files_path = list(filter(lambda file_path: file_path.endswith('.log'), listdir(path)))
        files_path = [ path_join(path, log_file_path) for log_file_path in log_files_path]
        for file_path in files_path:
            log_lines += read_file_lines(file_path)

    # if path is a file then extract log lines
    elif isfile(path):
        log_lines = read_file_lines(path)

    # if file/dir is not present then raise error
    else:
        raise FileNotFoundError(f'{path} log file/files not found.')
    
    return log_lines
