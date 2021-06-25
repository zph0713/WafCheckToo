import __init__
import os
import sys
import json
import re
import socket
import subprocess
from common.local_info import LocalInfomation
from conf import settings
from conf.settings import logger


class InstallGateWay():
    def __init__(self):
        self.un_i_resolv()
        self.host_ip = LocalInfomation().ip_addr

    def get_config(self,file_path):
        with open(file_path,'r') as target:
            return json.load(target)

    def set_host(self,ip,host):
        ip_host = "{} {}".format(ip,host)
        print(ip_host)
        #echo "xx.xx.xx.xx waf-test.xxx.com"|sudo tee -a /etc/hosts
        #cmd = ['echo',ip_host,'|','sudo','tee','-a','/etc/hosts']
        cmd2 = 'echo "{}"|sudo tee -a /etc/hosts'.format(ip_host)
        #result = subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
        result = subprocess.run(cmd2,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
        if result.returncode == 0:
            logger.debug(result)
            logger.info("success")
        else:
            logger.debug(result)
            logger.info("failed")

    def generator_config(self,group_name):
        logger.info('..generator command parameter')
        main_config = self.get_config(settings.main_config)
        config = self.get_config(settings.gateway_config)['gateway_group_info'][group_name]
        config = dict(config,**self.get_config(settings.gateway_config)['gateway_info'])
        self.set_host(self.host_ip,config['waf_hostname'])
        template = settings.gateway_template
        real_config = dict(main_config,**config)
        with open(template,'r') as target:
            pattern = re.compile(r'@(.*)@')
            tempf = target.read()
            rep = re.findall(pattern,tempf)
            logger.info('..now replace template infomation')
            for i in rep:
                src_key = '@'+i+'@'
                tempf = tempf.replace(src_key,real_config[i])
            return tempf

    def build_command(self,group_name):
        logtext = '..generator install command for {}'.format(group_name)
        logger.info(logtext)
        sub_command = ['sudo']
        command = os.path.join(settings.install_command_path,'ec2_auto_ftl')
        args_raw = self.generator_config(group_name)
        sub_command.append(command)
        args_list = list()
        for ags in args_raw.split():
            args_list.append(ags)
        sub_command.extend(args_list)

        logger.info(sub_command)
        return sub_command

    def un_i_resolv(self):
        logger.info("unset resolv i attribute")
        command = ['sudo','chattr','-i','/etc/resolv.conf']
        result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
        if result.returncode == 0:
            logger.debug(result)
            logger.info("success")
        else:
            logger.debug(result)
            logger.info("failed")


    def run_install(self,group_name):
        logger.info('..start run install')
        result = subprocess.run(self.build_command(group_name),stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
        if result.returncode == 0:
            logger.debug(result)
            logger.info("install success")
        else:
            logger.debug(result)
            logger.info("error,install failed")
