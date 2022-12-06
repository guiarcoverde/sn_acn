import os
import requests
import json

def endpoints(sys_id=None, userid=None) -> dict:
    api = os.environ.get('servicenow_api')
    return {
        'ticket_creation': f'{api}/incident',
        'ticket_mod':f'{api}/incident/{sys_id}',      
        'user_sys_id':f'{api}/sys_user?sysparm_query=user_name%3D{userid}'

    }

def process_data(data, type_func):
    if type_func == 'ticket_creation':
        data.setdefault('short_description', 'test')
        data.setdefault('caller_id', '')
        data.setdefault('urgency', 2)
    
    elif type_func == 'ticket_update':
        data.setdefault('close_code', '')
        data.setdefault('work_notes', '')
         
    return data

def ticket_creation(user, pwd, data):
    #Ticket creation
    data = process_data(data, type_func='ticket_creation')
    creation_endpoint = endpoints()['ticket_creation']

    headers = {"Content-Type":"application/json","Accept":"application/json"}
    data_form = '{'+'''\"short_description\":\"{}\",
                    \"caller_id\":\"{}\",
                    \"urgency\":\"{}\"
                    '''.format(data['short_description'], 
                                                  data['caller_id'],
                                                  data['urgency'])+'}'
    
    response = requests.post(creation_endpoint, auth=(user, pwd), headers=headers, data=data_form)
    response_data = {'status_code':response.status_code, 
                     'message':'Incident created sucessfully'}

    if response.status_code != 201: 
        response_data['message'] = 'Incident could not be created'
    
    
    return response_data
    



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

def creation(user, pwd, sd, urg):
    caller = get_caller_id(user=user, pwd=pwd, data={'userid':user})
    ticket_crea =  ticket_creation(user=user, pwd=pwd, data={'caller_id':caller, 'short_description':sd, 'urgency':urg})
    return ticket_crea
if __name__ == "__main__":
    # r1 = ticket_creation(user='admin', pwd='8Koc+BdG$l5R', data={'caller_id':'62826bf03710200044e0bfc8bcbe5df1', 'short_description':'TICKET NOVO 2'})
    # r2 = creation(user='abraham.lincoln', pwd='F1nnTroll!', sd='TICKET NOVO 6', urg=1)
    r3 = get_caller_id(user='admin', pwd='8Koc+BdG$l5R', data={'userid':'arron.ubhi'})
    print(json.dumps(r3, indent=1))