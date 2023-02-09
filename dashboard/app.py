from pandas import json_normalize, DataFrame
from elb_log_analyzer.log_analyzer import LogAnalyzer

import streamlit as st

st.set_page_config(layout='wide', page_title='ELB Log Analyzer Dashboard')

st.write('# ELB-Log-Analyzer Dashboard')
path = st.text_input('Enter Log Directory/File Path')
if len(path) == 0:
    st.write('Required!')
    pass

# path = r'D:\GithubRepos\elb-log-analyzer\logs\1.log'
log_analyzer = LogAnalyzer(log_file_path=path)

# load analyzed data into data frame
df = json_normalize(log_analyzer.logs)

# create bar chart for each ip
st.markdown('### Client Request Time (Can be used for Detecting DDoS/Bruteforce Attacks')
st.bar_chart(df, x='client_ip', y='timestamp', height=480)

# for total request count
st.markdown('### Client URL Hit Count')
requests_count = log_analyzer.count_request_by_client_ip()
requests_count = [ [client_ip,requests_count[client_ip]] for client_ip in requests_count.keys()]

request_df = DataFrame(requests_count, columns=['client_ip', 'requests_count'])
st.bar_chart(request_df, x='client_ip', y='requests_count')

# load analyzed data into df
analyzed_data = log_analyzer.analyzed_logs

# create table for client ip, total_requests, ports, user_agents
st.markdown('''
### Client Request Summary
Search for below keywords to find bots:
- bot
- headless
- requests
- axios
- node-fetch
''')
client_request_details = []
for client_ip in analyzed_data.keys():
    if client_ip == 'total':
        continue
    
    tot_req_count = analyzed_data[client_ip]['total']
    ports = ', '.join([str(port) for port in analyzed_data[client_ip]['ports']])
    user_agents = '\n'.join(analyzed_data[client_ip]['user_agents'])

    client_request_details.append([client_ip, tot_req_count, ports, user_agents])

client_req_df = DataFrame(client_request_details, columns=['client_ip', 'total_request_count', 'ports', 'user agents'])
st.table(client_req_df.sort_values(by=['total_request_count'], ascending=False))

# TODO: create table for client ip and abuse data (only for ips greater than threshold)


# TODO: create table for client ip and urls data.

# plot data into a table
# st.table(df)