from pandas import DataFrame
from json import loads
from utils import get_client_requests_count, get_data

import streamlit as st

st.set_page_config(layout='wide', page_title='ELB Log Analyzer Dashboard')

st.write('# ELB-Log-Analyzer Dashboard')
path = st.text_input('Enter Log File Path')
if path == '' or not path:
    st.write('Required!')
    st.stop()


# load analyzed logs into analyzer
with open(path, 'r') as f:
    analyzed_data = loads(f.read())

# create bar chart for each ip
# st.markdown(
    # '### Client Request Time (Can be used for Detecting DDoS/Bruteforce Attacks')
# st.bar_chart(timestamp_df, x='client_ip', y='timestamp', height=480)

# for total request count
st.markdown('### Client URL Hit Count')
requests_count = get_client_requests_count(analyzed_data)
# convert to list
requests_count = [[client_ip, requests_count[client_ip]]
                  for client_ip in requests_count.keys()]

request_df = DataFrame(requests_count, columns=['client_ip', 'requests_count'])
st.bar_chart(request_df, x='client_ip', y='requests_count')


# create table for client ip, total_requests, ports, user_agents
st.markdown('''
### Client Request Summary
Search for below keywords to find bots:
- bot
- headless
- requests
- axios
- node-fetch
- requests
''')
client_request_details = []
http_req_details = []
for client_ip in analyzed_data.keys():
    if client_ip == 'total':
        continue

    # for client_req_df
    tot_req_count = analyzed_data[client_ip]['total']
    ports = ', '.join([str(port)
                      for port in analyzed_data[client_ip]['ports']])
    user_agents = '\n'.join(analyzed_data[client_ip]['user_agents'])

    client_request_details.append(
        [client_ip, tot_req_count, ports, user_agents])

    # for http_req_df
    http_requests = analyzed_data[client_ip]['requests']
    get = '\n'.join(get_data(http_requests.get('GET', {})))
    post = '\n'.join(get_data(http_requests.get('POST', {})))
    put = '\n'.join(get_data(http_requests.get('PUT', {})))
    patch = '\n'.join(get_data(http_requests.get('PATCH', {})))
    delete = '\n'.join(get_data(http_requests.get('DELETE', {})))
    options = '\n'.join(get_data(http_requests.get('OPTIONS', {})))

    http_req_details.append([client_ip, get, post, put, patch, delete, options])


# plot user data
client_req_df = DataFrame(client_request_details, columns=[
                          'client_ip', 'total_request_count', 'ports', 'user agents'])
st.table(client_req_df.sort_values(
    by=['total_request_count'], ascending=False))


# plot user requested urls
st.markdown('''
### Client URLs list
''')

http_req_df = DataFrame(http_req_details, columns=['client_ip', 'GET','POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
st.table(http_req_df)