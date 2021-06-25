import __init__
from core.main_process import MainProcess
import argparse
from conf.settings import logger


def war_manager():
    parser = argparse.ArgumentParser(add_help=True,description='WafCheckToo')
    parser.add_argument('-I','--install_ec2',help="install_ec2")
    parser.add_argument('-C','--haproxy_config',action="store_true",help="generator haproxy config to etc")
    parser.add_argument('-i','--imperva_ctrl',help="imperva ctrl")
    parser.add_argument('-A','--imperva_after_install',action="store_true",help="imperva_after_install")
    parser.add_argument('-ac','--add_crontab',action="store_true",help="add crontab")
    parser.add_argument('-S','--add_reboot_crontab',help="add reboot crontab")

    obj = parser.parse_args()
    MP = MainProcess()
    if obj.install_ec2:
        MP.install_gateway(obj.install_ec2)
    elif obj.haproxy_config:
        MP.generator_haproxy_config()
        MP.replace_haproxy_config()
        MP.restart_haproxy()
    elif obj.imperva_ctrl:
        MP.imperva_ctrl(obj.imperva_ctrl)
    elif obj.imperva_after_install:
        MP.imperva_ctrl('service_stop')
        MP.imperva_ctrl('gw_unreg')
        MP.imperva_ctrl('gw_config')
        MP.imperva_ctrl('service_start')
        MP.imperva_ctrl('platform_config')
    elif obj.add_crontab:
        MP.add_crontab()
    elif obj.add_reboot_crontab:
        print(obj.add_reboot_crontab)
        MP.add_reboot_crontab(obj.add_reboot_crontab)
    else:
        exit(1)

if __name__ == '__main__':
    war_manager()
