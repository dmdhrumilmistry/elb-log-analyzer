# ELB Log Analyzer

Tool for analyzing ELB logs.

## Installation

- Using Pip

    ```bash
    python3 -m pip install elb-log-analyzer
    ```

## Usage

- Print help Menu

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

## Publish package to pypi

- Using poetry

    ```bash
    python3 -m poetry publish --build --username [PYPI_USERNAME] --password [PYPI_PASSWORD]
    ```
