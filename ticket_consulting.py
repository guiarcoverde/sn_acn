import requests
import os
import json

def endpoints(inc_number=None,inc_caller=None, userid=None) -> dict:
    api = os.environ.get('servicenow_api')
    return {
        'list_incident_number': f'{api}/incident?sysparm_query=number%3D{inc_number}',
        'incident_per_user':f'{api}/incident?sysparm_query=caller_id%3D{inc_caller}',
        'user_sys_id':f'{api}/sys_user?sysparm_query=user_name%3D{userid}'      
    }



def ticket_consulting_number(user, pwd, data):
    endpoint = endpoints(inc_number = data['inc_number'])['list_incident_number']

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    response = requests.get(endpoint, auth=(user, pwd), headers=headers )

    data_return = {
        'status_code':response.status_code,
        'content':[]
    }
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    else:
        data = response.json()
        data_result = data['result']
        for d in data_result:
            my_data = {'Caller':d["caller_id"],
                        'Incident Number':d['number'],
                        'Short Description':d['short_description'],
                        'Description':d['description'],
                        }
            data_return['content'].append(my_data)
    
    return data_return



def ticket_consulting_user(user, pwd, data):
    endpoint = endpoints(inc_caller = data['inc_caller'])['incident_per_user']

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    response = requests.get(endpoint, auth=(user, pwd), headers=headers )

    data_return = {
        'status_code':response.status_code,
        'content':[]
    }
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    else:
        data = response.json()
        data_result = data['result']
        for d in data_result:
            my_data = {'Caller':d["caller_id"],
                        'Incident Number':d['number'],
                        'Short Description':d['short_description'],
                        'Description':d['description'],
                        }
            data_return['content'].append(my_data)
    
    return data_return

def get_caller_id(user, pwd, data):
    endpoint = endpoints(userid = data['userid'])['user_sys_id']

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    response = requests.get(endpoint, auth=(user, pwd), headers=headers)
    data_return = {
        'status_code':response.status_code,
        'content':[]
    }
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    else:
        data = response.json()
        data_result = data['result']
        my_data = {'user_name':'none', 'sys_id': 'none'}
        for d in data_result:
            my_data = {'Username':d['user_name'],
                        'User ID':d['sys_id'],
            }
            data_return['content'].append(my_data)
    assert len(data_return['content']) == 1, 'USER COULD NOT BE RETRIEVED'
    return data_return['content'][0]['User ID']

def inc_filter_by_caller(name, user, pwd):
    callers = get_caller_id(user=user, pwd=pwd, data={'userid':name})
    inc_filter = ticket_consulting_user(user=user, pwd=pwd, data={'inc_caller':callers})
    
    return inc_filter


if __name__ == '__main__':
    number_filter = ticket_consulting_number(user='admin', pwd='8Koc+BdG$l5R', data={'inc_number':'INC0010030'}) 
    caller_filter = inc_filter_by_caller(name='abraham.lincoln', user='admin', pwd='8Koc+BdG$l5R')
    print(json.dumps(number_filter, indent=1))