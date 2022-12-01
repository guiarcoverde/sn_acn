import os
import requests
import json

def endpoints(sys_id=None) -> dict:
    api = os.environ.get('servicenow_api')
    return {
        'ticket_creation': f'{api}/incident',
        'ticket_mod':f'{api}/incident/{sys_id}',      
        'delete_ticket':f'{api}/incident/{sys_id}'

    }

def process_data(data, type_func):
    if type_func == 'ticket_creation':
        data.setdefault('short_description', 'test')
        data.setdefault('description', 'test')
        data.setdefault('caller_id', '')
        data.setdefault('business_impact', 3)
        data.setdefault('business_service', '')
        data.setdefault('service_offering', '')
        data.setdefault('impact', 2)
        data.setdefault('urgency', 2)
        data.setdefault('category', '')
        data.setdefault('subcategory', '')
        data.setdefault('location', '')
        data.setdefault('cmdb_ci', '')   
    
    elif type_func == 'ticket_update':
        data.setdefault('caller_id', '')
        data.setdefault('business_service', '')
        data.setdefault('service_offering', '')
        data.setdefault('close_code', '')
        data.setdefault('work_notes', '')
        data.setdefault('cmdb_ci', '')

    return data

def ticket_creation(user, pwd, data):
    #Ticket creation
    data = process_data(data, type_func='ticket_creation')
    creation_endpoint = endpoints()['ticket_creation']

    headers = {"Content-Type":"application/json","Accept":"application/json"}
    data_form = '{'+'''\"short_description\":\"{}\",
                    \"description\":\"{}\",
                    \"caller_id\":\"{}\",
                    \"assigned_to\":\"\",
                    \"assignment_group\":\"\",
                    \"business_impact\":\"{}\",
                    \"business_service\":\"{}\",
                    \"service_offering\":\"{}\",
                    \"impact\":\"{}\",
                    \"urgency\":\"{}\",
                    \"category\":\"{}\",
                    \"subcategory\":\"{}\",
                    \"location\":\"{}\",
                    \"cmdb_ci\":\"{}\"'''.format(data['short_description'], 
                                                  data['description'], 
                                                  data['caller_id'],
                                                  data['business_impact'],
                                                  data['business_service'],
                                                  data['service_offering'],
                                                  data['impact'],
                                                  data['urgency'],
                                                  data['category'],
                                                  data['subcategory'],
                                                  data['location'],
                                                  data['cmdb_ci'])+'}'
    
    response = requests.post(creation_endpoint, auth=(user, pwd), headers=headers, data=data_form)
    response_data = {'status_code':response.status_code, 
                     'message':'Incident created sucessfully'}

    if response.status_code != 201: 
        response_data['message'] = 'Incident could not be created'
    
    
    return response_data
    

def ticket_update(user, pwd, data):
    data = process_data(data, type_func='ticket_update')
    mod_endpoint = endpoints(data['sys_id'])['ticket_mod']

    headers = {"Content-Type":"application/json","Accept":"application/json"}
    data_form = '{'+'''\"caller_id\":\"{}\",
                    \"assigned_to\":\"\",
                    \"assignment_group\":\"\",
                    \"business_service\":\"{}\",
                    \"service_offering\":\"{}\",
                    \"cmdb_ci\":\"{}\",
                    \"close_code\":\"{}\",
                    \"work_notes\":\"{}\"'''.format(data['caller_id'],
                                                 data['business_service'],
                                                  data['service_offering'],
                                                  data['cmdb_ci'],
                                                  data['close_code'],
                                                  data['work_notes'])+'}'

    response = requests.put(mod_endpoint, auth=(user, pwd), headers=headers ,data=data_form)
    response_data = {'status_code':response.status_code, 
                     'message':'Incident updated sucessfully'}


    if response.status_code != 200: 
        response_data['message'] = 'Error when trying to update the incident'

    return response_data

def ticket_delete(user, pwd, data):
    delete_endpoint = endpoints(data['sys_id'])['delete_ticket']

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    response = requests.delete(delete_endpoint, auth=(user, pwd), headers=headers )
    response_data = {'status_code':response.status_code,
                     'message': 'Incident was sucessfully deleted'}
    if response.status_code != 204: 
        response_data['message'] = 'Could not delete the incident'

    return response_data


if __name__ == "__main__":

    
    r1 = ticket_delete(user='admin', pwd='8Koc+BdG$l5R', data={'sys_id':'22f78cb897a71110e15c78300153afbb'})
    print(json.dumps(r1, indent=1))
