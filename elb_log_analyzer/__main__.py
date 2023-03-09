from pprint import pprint
from argparse import ArgumentParser
from json import dumps

from .log_analyzer import LogAnalyzer


parser = ArgumentParser(prog='elb-log-analyzer')
parser.add_argument('-i', '--input-log-file', dest='log_file_path',
                    help='Log file path or path of directory storing only log files', type=str, required=True)
parser.add_argument('-k', '--api-key', dest='api_key',
                    help='Abuse IP DB API key', type=str, default=None)
parser.add_argument('-t', '--threshold',
                    dest='request_threshold', default=40, type=int)
parser.add_argument('-o', '--output', help='output file path for storing data in json format',
                    dest='output_file_path', type=str, default=None)
args = parser.parse_args()

# analyze logs
log_analyzer = LogAnalyzer(log_file_path=args.log_file_path,
                           ipabuse_api_key=args.api_key, request_threshold=args.request_threshold)
analyzed_data = log_analyzer.analyze_logs()

# write/print data
out_file_path = args.output_file_path
if out_file_path:
    with open(out_file_path, 'w') as f:
        f.write(dumps(analyzed_data))
        print(f'Analyzed Data stored in file: {out_file_path}')
else:
    pprint(analyzed_data)
