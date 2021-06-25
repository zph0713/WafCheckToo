import __init__
import os
import subprocess
import time
from crontab import CronTab
from conf import settings
from conf.settings import logger



class CronTabCtrl(object):
    def __init__(self):
        self.ha_script_path = os.path.join(settings.scriptsDir,'check_ha.sh')
        self.reboot_script_path = os.path.join(settings.scriptsDir,'restart_server.sh')
        self.tar_scripts_path = settings.script_path
        self.mk_dir()
        self.mv_scripts()
        self.ha_cron_path = os.path.join(settings.script_path,'check_ha.sh')
        self.reboot_cron_path = os.path.join(settings.script_path,'restart_server.sh')
        self.chmod_scripts()

    def mk_dir(self):
        cmd = ['sudo','mkdir','-p',settings.script_path]
        deploy = subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=5)
        if deploy.returncode == 0:
            logger.info("mkdir success")
        else:
            logger.debug(deploy1)
            logger.info("mkdir error")

    def src_scripts_path(script_name):
        return os.path.join(settings.scriptsDir,script_name)

    def mv_scripts(self):
        cmd1 = ['sudo','cp','-rp',self.ha_script_path,self.tar_scripts_path]
        cmd2 = ['sudo','cp','-rp',self.reboot_script_path,self.tar_scripts_path]

        deploy1 = subprocess.run(cmd1,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=5)
        if deploy1.returncode == 0:
            logger.info("mv ha_script success")
        else:
            logger.debug(deploy1)
            logger.info("mv ha_script error")

        deploy2 = subprocess.run(cmd2,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=5)
        if deploy2.returncode == 0:
            logger.info("mv reboot_script success")
        else:
            logger.debug(deploy2)
            logger.info("mv reboot_script error")

    def chmod_scripts(self):
        cmd1 = ['sudo','chmod','+x',self.ha_cron_path]
        cmd2 = ['sudo','chmod','+x',self.reboot_cron_path]

        deploy1 = subprocess.run(cmd1,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=5)
        if deploy1.returncode == 0:
            logger.info("chmod ha_script success")
        else:
            logger.debug(deploy1)
            logger.info("chmod ha_script error")

        deploy2 = subprocess.run(cmd2,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=5)
        if deploy2.returncode == 0:
            logger.info("chmod reboot_script success")
        else:
            logger.debug(deploy2)
            logger.info("chmod reboot_script error")

    def set_ha_cron(self):
        return self.set_crontab(self.ha_cron_path,'*/5 * * * *','check_ha')

    def set_reboot_cron(self,cron_time):
        m_time = cron_time.split('_')[0]
        h_time = cron_time.split('_')[1]
        reboot_cronttime = '{} {} * * *'.format(m_time,h_time)
        return self.set_crontab(self.reboot_cron_path,reboot_cronttime,'reboot_server')

    def set_crontab(self,script_path,crontime,comment_name):
        script_path = os.path.join(script_path)
        cron_manager  = CronTab(user='root')
        command_line = "sh {}".format(script_path)
        selfcron = list()
        for job in cron_manager:
            if job.comment == comment_name:
                job.setall(crontime)
                cron_manager.write()
                selfcron.append(job.comment)
            elif job.command == command_line:
                print(job)
                cron_manager.remove(job)
                cron_manager.write()
        if len(selfcron) == 0:
            job = cron_manager.new(command=command_line,comment=comment_name)
            job.setall(crontime)
            cron_manager.write()
