import os
import json
import requests

def endpoints(sys_id=None, inc_number=None, userid=None) -> dict:
    api = os.environ.get('servicenow_api')
    return {
        'list_incident_number': f'{api}/incident?sysparm_query=number%3D{inc_number}',
        'ticket_mod':f'{api}/incident/{sys_id}',
        'user_sys_id':f'{api}/sys_user?sysparm_query=user_name%3D{userid}'      
    }


def update_request(user, pwd, data):
    mod_endpoint = endpoints(data['sys_id'])['ticket_mod']

    headers = {"Content-Type":"application/json","Accept":"application/json"}
    data_form = '{'+'''\"assigned_to\":\"{}\",
                       \"work_notes\":\"{}\"'''.format(data['assigned_to'],
                                                       data['work_notes'])+'}'

    response = requests.put(mod_endpoint, auth=(user, pwd), headers=headers ,data=data_form)
    response_data = {'status_code':response.status_code, 
                     'message':'Incident updated sucessfully'}


    if response.status_code != 200: 
        response_data['message'] = 'Error when trying to update the incident'

    return response_data


def get_inc_id(user, pwd, data):
    endpoint = endpoints(inc_number=data['inc_number'])['list_incident_number']

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
        my_data = {'number':'none', 'sys_id': 'none'}
        for d in data_result:
            my_data = {'INC Number':d['number'],
                        'Ticket Number ID':d['sys_id'],
            }
            data_return['content'].append(my_data)
    assert len(data_return['content']) == 1, 'INC COULD NOT BE RETRIEVED'
    return data_return['content'][0]['Ticket Number ID']

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


def inc_update(user, pwd, name, inc, wn):
    callers = get_caller_id(user=user, pwd=pwd, data={'userid':name})
    id_extraction = get_inc_id(user=user, pwd=pwd, data={'inc_number':inc})
    update = update_request(user=user, pwd=pwd, data={'sys_id':id_extraction, 'assigned_to':callers, 'work_notes':wn })
    return update

if __name__ == '__main__':
    # r1 = get_inc_id(user='admin', pwd='8Koc+BdG$l5R', data={'inc_number':'INC0010046'})
    r2 = inc_update(user='admin', pwd='8Koc+BdG$l5R', name='arron.ubhi', inc='INC0010046', wn='ISTO É UM TESTE')
    # r3 = get_caller_id(user='admin', pwd='8Koc+BdG$l5R', data={'userid':'arron.ubhi'})
    print(json.dumps(r2, indent=1))