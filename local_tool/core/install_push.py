import __init__
import requests
import json
import os
import re
import time
from urllib.parse import urljoin
from core.get_token import executeToken
from conf import settings
from conf.settings import logger

class ExecuteDeploy(object):
    def __init__(self):
        self.execute_record = list()

    def split_execute(self,ip_list,post_params):
        logger.info('split execute..')
        task_name_prefix = 'imperva_install_'
        count = 0
        if post_params.startswith('-S'):
            num = len(ip_list)
            time_table = dict()
            for l in range(24):
                time_table[l] = list()
            for pp in range(num):
                ip = ip_list[pp]
                pp = pp%24
                time_table[pp].append(ip)
            logger.debug(time_table)
            split_time = dict()
            for k,v in time_table.items():
                step = 60//len(v)
                item_count = 0
                for p in range(0,60,step):
                    ip = list()
                    ip.append(v[item_count])
                    post_params = "-S {}_{}".format(p,k)
                    print(post_params)
                    split_task_name = task_name_prefix+str(count)
                    self.execute_deploy(split_task_name,ip,post_params)
                    logger.info("push reboot crontab")
                    item_count+=1
                    count+=1
                    time.sleep(2)
        else:
            for i in range(0,len(ip_list),2):
                count+=1
                split_task_name = task_name_prefix+str(count)
                split_ip_list = ip_list[i:i+2]
                print(split_task_name,split_ip_list)
                self.execute_deploy(split_task_name,split_ip_list,post_params)
                time.sleep(15)
        logger.info(self.execute_record)

    def execute_deploy(self,stn,sil,post_params):
        #list_ip = list()
        #list_ip.append(sil)
        logger.info('start push install..')
        headers = {'X-Token':executeToken(),'Content-Type':'application/json'}
        payload = {
            "script_id": 57,
            "params": post_params,
            "ip_list": sil,
            "task_name": stn,
            "trigger_type": "immediately"
        }
        logger.info(stn)
        logger.info(sil)
        logger.info(post_params)
        res = requests.post(settings.execute_url,headers=headers,data=json.dumps(payload),timeout=10)
        print(res.json())
        task_id = res.json()['info']['task_id']
        logger.info(task_id)
        self.execute_record.append(task_id)

    def echo_deploy_status(self,task_id_list):
        logger.info('show install status..')
        headers = {'X-Token':executeToken(),'Content-Type':'application/json'}
        for task_id in task_id_list:
            print(task_id)
            url = urljoin(settings.echo_excute_url,task_id) + '/'
            res = requests.get(url,headers=headers)
            results = res.json()['info']
            logger.debug(res.url)
            kv = dict()
            dkv = dict()
            for k,v in results.items():
                if k != 'task_details':
                    kv[k] = v
                else:
                    dkv[k] = v
            logger.info(kv)
            for detail in dkv['task_details']:
                logger.info(detail['stdout'])
                logger.error(detail['stderr'])
