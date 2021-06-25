import __init__
import shutil
import subprocess
from conf import settings
from conf.settings import logger


class HaproxyCtrl(object):
    def __init__(self):
        pass

    def mv_config(self):
        cmd = ['sudo','mv',settings.final_config_path,settings.haproxy_config_path]
        deploy = subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=5)
        if deploy.returncode == 0:
            logger.debug(deploy)
            logger.info("success")
        else:
            logger.debug(deploy)
            logger.info("error")

    def restart_haproxy(self):
        cmd = ['sudo','systemctl','restart','haproxy']
        restart = subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=5)
        if restart.returncode == 0:
            logger.debug(restart)
            logger.info("success")
        else:
            logger.debug(restart)
            logger.info("error")
            
