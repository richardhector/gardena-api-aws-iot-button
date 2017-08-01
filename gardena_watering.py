# please fill in login_email and pw with your gardena credentials

import requests, json, ast

# mock app with API calls https://sg-api.dss.husqvarnagroup.net/sg-1/index/ios/
# documentation http://www.roboter-forum.com/showthread.php?16777-Gardena-Smart-System-Analyse

gardena_api_url = "https://sg-api.dss.husqvarnagroup.net/sg-1"
login_email = ''
pw = ''
watering_in_mins = "1"

def login(email, password):
    headers = {"content-type": "application/json"}
    data = ast.literal_eval("""{'sessions': {'email': '""" + email + """','password': '""" + password + """'}}""")
    r = requests.post(gardena_api_url + """/sessions""", data=json.dumps(data), headers=headers)
    details = json.loads(r.text)
    user_id = details['sessions']['user_id']
    token = details['sessions']['token']
    return user_id, token

def get_locations(user_id, token, headers):
    r = requests.get(gardena_api_url + """/locations/?user_id=""" + user_id, headers=headers)
    my_locations = json.loads(r.text)
    return my_locations

def get_devices(location_id, headers):
    r = requests.get(gardena_api_url + """/devices?locationId=""" + location_id, headers=headers)
    devices = json.loads(r.text)
    return devices

def get_device_id(devices, dev_type):
    for i in devices.keys():
        for j in devices[i]: 
            if dev_type == j["category"]:
                return j["id"]
            
def start_watering (device_id, headers):
    data = ast.literal_eval("""{'name':'manual_override','parameters':{'manual_override':'open','duration':""" + watering_in_mins + """}}""")
    url_r = gardena_api_url + """/devices/""" + device_id + """/abilities/outlet/command?locationId=""" + location_id
    r = requests.post(url_r, data=json.dumps(data), headers=headers)
    # check if watering worked
    if r.status_code == 204:
        print("Watering for " + watering_in_mins + " minutes")
    elif r.status_code == 503:
        print("Error, try again in 3 minutes")
    else:
        print(r.text)
    return r

def stop_wartering():
    data = {"name":"cancel_override","parameters":{}}
    url_r = gardena_api_url + """/devices/""" + device_id + """/abilities/outlet/command?locationId=""" + location_id
    r = requests.post(url_r, data=json.dumps(data), headers=headers)
    if r.status_code == 204:
        print("Stopped watering")
    elif r.status_code == 503:
        print("Error, try again in 3 minutes")
    else:
        print(r.text)
    return r


#login in
login_details = login(login_email, pw)

#global variables
user_id = login_details[0]
token = login_details[1]
headers = ast.literal_eval("""{'content-type': 'application/json','X-Session': '""" + token + """'}""")

my_locations = get_locations(user_id, token, headers)

#get locations
location_id = my_locations['locations'][0]['id']

#get devices
devices = get_devices(location_id, headers)

# get device_id of water controller
device_id = get_device_id(devices, 'watering_computer')


start_watering(device_id, headers)

#stop_wartering()
