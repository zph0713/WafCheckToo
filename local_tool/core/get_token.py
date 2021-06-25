import __init__
import requests,urllib3,json
from urllib.parse import urljoin
from conf import settings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def impervaCookie():
    user,pswd = settings.imperva_user,settings.imperva_password
    gettoken_url = urljoin(settings.imperva_url,settings.token_api)
    r = requests.post(gettoken_url,auth=(user,pswd),verify=False)
    session_id = r.json()['session-id']
    return session_id

def cmdbToken():
    return settings.cmdb_token

def executeToken():
    return settings.execute_token

if __name__ == "__main__":
    impervaToken()
