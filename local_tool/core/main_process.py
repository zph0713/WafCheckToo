import __init__
from core.install_ec2_auto_ftl import InstallGateWay
from core.haproxy_conf_generator import HaproxyConf
from core.haproxy_ctrl import HaproxyCtrl
from core.format_data import config_viewer
from core.waf_status_check import WafCheck
from core.imperva_ctrl import ImpervaCtrl
from conf import settings
from conf.settings import logger


class MainProcess(object):
    def __init__(self):
        self.IG = InstallGateWay()
        self.HC = HaproxyConf()
        self.HCT = HaproxyCtrl()
        self.WC = WafCheck()
        self.IC = ImpervaCtrl()

    def install_gateway(self,group_name):
        return self.IG.run_install(group_name)

    def generator_haproxy_config(self):
        return self.HC.generator_config()

    def view_haproxy_config(self,config_type):
        if config_type == 'current':
            config_viewer(settings.current_config_path)
        elif config_type == 'backup':
            config_viewer(settings.backup_config_path)
        elif config_type == 'new':
            config_viewer(settings.final_config_path)
        else:
            print('exit  example: {current|backup|new}')

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
