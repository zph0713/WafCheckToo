import __init__
import requests
import json
from urllib.parse import urljoin
from conf import settings
from core.get_token import impervaCookie
from conf.settings import logger


class ImpervaApi(object):
    def __init__(self):
        self.gw_ip_list = list()

    def get_gateway_info(self):
        logger.info("get imperva gateway ip")
        headers = {'Content-Type': 'application/json',
                    'Cookie': f'{impervaCookie()}'}
        url = urljoin(settings.imperva_url,settings.gateway_api)
        res = requests.get(url,headers=headers)
        gw_list = res.json()['gateways']
        #for gw in gw_list:
        #    print(gw)
            #self.gw_ip_list.append[gw['ip']]
        return gw_list
