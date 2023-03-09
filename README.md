# ELB Log Analyzer

Tool for analyzing ELB logs for automating steps to retreive details of ip's user agent, total request count, to which urls requests were made along with their total count, and http methods in json format.

## S3 Bucket Log Downloader

Downloads S3 bucket objects that we created in specified time window.

## Installation

- Using Pip

    ```bash
    python3 -m pip install elb-log-analyzer
    ```

### AWS configuration

- Create IAM policy with below configuration

    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3ListSpecificDirectory",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::alb-log-bucket-name"
        },
        {
            "Sid": "S3GetSpecificDirectory",
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/*"
        }
    ]
    }
    ```

    > **Note**: above policy will allow user to list all contents in the bucket but download objects only from `s3://alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/*`

- Create AWS access keys

- Use aws cli to configure access key for boto3

    ```bash
    aws configure
    ```

### S3 Bucket Log Downloader Usage

- Print Help Menu.

    ```bash
    python3 -m elb_log_analyzer.s3_log -h
    ```

- Download all log files generated in 10 hours from now.

    ```bash
    python3 -m elb_log_analyzer.s3_log -b elb-log-bucket -p 'alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/' -H 10
    ```

- Download all log files generated in 40 mins from now.

    ```bash
    python3 -m elb_log_analyzer.s3_log -b elb-log-bucket -p 'alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/' -m 40
    ```

- Download all log files generated in 20 secs from now.

    ```bash
    python3 -m elb_log_analyzer.s3_log -b elb-log-bucket -p 'alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/' -s 20
    ```

- Download all log files generated in 10 hours, 40 mins and 20 secs from now and store in a directory.

    ```bash
    python3 -m elb_log_analyzer.s3_log -b elb-log-bucket -p 'alb-log-bucket-name/AWSLogs/XXXXXXXXXXXX/elasticloadbalancing/aws-region/' --hours 10 --minutes 40 --seconds 20 -o './logs/downloads'
    ```

## Analyzer

Analyzes downloaded log files.

### Analyzer Usage

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
    python3 -m elb_log_analyzer -i [LOG_FILE_PATH] -t [REQUESTS_THRESHOLD_VALUE] -k [IP_ABUSE_DB_API_KEY] -o [OUTPUT_FILE_PATH]
    ```

## Dashboard

Dashboard to visualize data.

### Dashboard Installation

- Install requirements

    ```bash
    python3 -m pip install dashboard/requirements.txt
    ```

### Usage

- Start App

    ```bash
    streamlit run dashboard/app.py
    ```

- Enter Log File/Directory Path

## Publish package to pypi

- Using poetry

    ```bash
    python3 -m poetry publish --build --username [PYPI_USERNAME] --password [PYPI_PASSWORD]
    ```
