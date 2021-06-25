import __init__
import subprocess
from common.local_info import LocalInfomation
from conf import settings
from conf.settings import logger


class ImpervaCtrl(object):
    def __init__(self):
        self.host_ip = LocalInfomation().ip_addr

    def impctl_ctrl(self,action):
        logstext = "impctl ctrl action: {}".format(action)
        logger.info(logstext)
        impctl_cmd = settings.imperva_ctl_command
        ip_name = '--name=gw'+self.host_ip.replace('.','_')
        if action == 'service_stop':
            command = [impctl_cmd,'service','stop','--transient','gateway']
        elif action == 'gw_unreg':
            command = [impctl_cmd,'gateway','unregister']
        elif action == 'gw_config':
            command = [impctl_cmd,'gateway','config',ip_name]
        elif action == 'service_start':
            command = [impctl_cmd,'service','start','--transient','gateway']
        elif action == 'platform_config':
            command = ['sudo','-i',impctl_cmd,'platform','host','config',ip_name]
        elif action == 'check_gateway_status':
            command = [impctl_cmd,'gateway','status']
        else:
            exit(1)
        print(command)
        ret = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
        if ret.returncode == 0:
            logger.info("success")
        else:
            logger.info("error")
        logger.debug(ret)
