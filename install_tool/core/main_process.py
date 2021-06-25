import __init__
from core.install_ec2_auto_ftl import InstallGateWay
from core.haproxy_conf_generator import HaproxyConf
from core.haproxy_ctrl import HaproxyCtrl
from core.imperva_ctrl import ImpervaCtrl
from core.cronjob_set import CronTabCtrl
from conf import settings
from conf.settings import logger


class MainProcess(object):
    def __init__(self):
        self.IG = InstallGateWay()
        self.HC = HaproxyConf()
        self.HCT = HaproxyCtrl()
        self.IC = ImpervaCtrl()
        self.CTC = CronTabCtrl()

    def install_gateway(self,group_name):
        return self.IG.run_install(group_name)

    def generator_haproxy_config(self):
        return self.HC.generator_config()

    def replace_haproxy_config(self):
        return self.HCT.mv_config()

    def rollback_haproxy_config(self):
        return self.HCT.rollback_config()

    def restart_haproxy(self):
        return self.HCT.restart_haproxy()

    def check_waf_status(self):
        return self.WC.show_waf_check()

    def imperva_ctrl(self,action):
        return self.IC.impctl_ctrl(action)

    def add_crontab(self):
        return self.CTC.set_ha_cron()

    def add_reboot_crontab(self,cron_time):
        return self.CTC.set_reboot_cron(cron_time)
