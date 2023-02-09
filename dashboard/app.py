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

# Table to print urls
# plot data into a table
# st.table(df)