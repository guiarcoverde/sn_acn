from sanic import Sanic
from sanic import response
import json
from ticket_consulting import api_table
import traceback

app = Sanic("SNtoFrameworkTest")

@app.post("/incidents-list")
async def route_list(request):
    response_request = []
    msv = 200
    
    try:
        print(request.body)
        data_received = json.loads(request.body)
        usr = data_received['user']
        pwd = data_received['pwd']

        response_request = api_table(usr, pwd)
    except KeyError:
        traceback.print_exc()
        msv = 701
    except:
        msv = 404
    
    return response.json(
        response_request,
        headers={'X-Served-By': 'sanic'},
        status=msv
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181)