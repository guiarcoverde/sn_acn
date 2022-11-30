import os
import requests
import json

def endpoints() -> dict:
    api = os.environ.get('servicenow_api')
    return {
        'ticket_creation': f'{api}/incident?sysparm_limit=10',
        'ticket_mod':f'{api}/incident/sys_id',      
        'delete_ticket':f'{api}/incident/sys_id'

    }


def ticket_definition(user, pwd):
    #Ticket creation
    creation_endpoint = endpoints()['ticket_creation']

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    response = requests.post(creation_endpoint, auth=(user, pwd), headers=headers ,data="{\"short_description\":\"test\",\"description\":\"test\",\"caller_id\":\"sys_user\",\"assigned_to\":\"\",\"assignment_group\":\"\",\"business_impact\":\"work_impact\",\"business_service\":\"type_of_service\",\"service_offering\":\"service_offered\",\"impact\":\"impact_of_service\",\"urgency\":\"urgency_of_service\",\"category\":\"category\",\"subcategory\":\"subcat\",\"location\":\"user_loc\",\"cmdb_ci\":\"user_product\"}")

    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

    creation_data = response.json()
    

    #Ticket Update
    mod_endpoint = endpoints()['ticket_mod']

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    response = requests.put(mod_endpoint, auth=(user, pwd), headers=headers ,data="{\"caller_id\":\"\",\"assignment_group\":\"\",\"assigned_to\":\"\",\"business_service\":\"\",\"service_offering\":\"\",\"cmdb_ci\":\"\",\"close_code\":\"\",\"work_notes\":\"\"}")

    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

    mod_data = response.json()

    #Ticket Delete
    delete_endpoint = endpoints()['delete_ticket']

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    response = requests.delete(delete_endpoint, auth=(user, pwd), headers=headers )

    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

    delete_data = response.json()
    
    return creation_data, mod_data, delete_data

if __name__ == '__main__':
    ticket_definition(user='admin', pwd='8Koc+BdG$l5R')
