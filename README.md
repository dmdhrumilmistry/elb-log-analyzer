# ELB Log Analyzer

Tool for analyzing ELB logs for automating steps to retreive details of ip's user agent, total request count, to which urls requests were made along with their total count, and http methods in json format.

## Installation

- Using Pip

    ```bash
    python3 -m pip install elb-log-analyzer
    ```

## Usage

- Print Help Menu

    ```bash
    python3 -m elb_log_analyzer -h
    ```

- Print json data on console

    ```bash
    python3 -m elb_log_analyzer -i [INPUT_LOG_FILE_PATH]
    ```

- Store json data in a file

    ```bash
    python3 -m elb_log_analyzer -i [INPUT_LOG_FILE_PATH] -o [OUTPUT_FILE_PATH]
    ```

    > **Note**: **INPUT_LOG_FILE_PATH** can be log file or a directory containing all log files ending with `.log` extension

- Get IP details from IPAbuseDB

    ```bash
    python3 -m elb_log_analyzer -i [LOG_FILE_PATH] -t 3 -k [IP_ABUSE_DB_API_KEY] -o analyzed-data.json
    ```

## Publish package to pypi

- Using poetry

    ```bash
    python3 -m poetry publish --build --username [PYPI_USERNAME] --password [PYPI_PASSWORD]
    ```
