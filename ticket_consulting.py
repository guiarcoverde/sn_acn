import requests
import os
import json

def endpoints() -> dict:
    api = os.environ.get('servicenow_api')
    return {
        'list_incident': f'{api}/incident?sysparm_limit=10'      
    }



def api_table(user, pwd):
    endpoint = endpoints()['list_incident']
    url = endpoint

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    response = requests.get(url, auth=(user, pwd), headers=headers )

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
            my_data = {'Title':d["short_description"],
                        'Made the SLA':d['made_sla'],
                        'Incident Number':d['number'],
                        'Assigned To:':d['assigned_to'],
                        'Resolved by:':d['resolved_by']}
            data_return['content'].append(my_data)
    
    return data_return

# API_TABLE FUNCTION TESTING
if __name__ == '__main__':
    test = api_table(user='admin', pwd='8Koc+BdG$l5R')
    print(json.dumps(test, indent=1))