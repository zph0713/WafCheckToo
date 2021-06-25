import __init__
from core.install_push import ExecuteDeploy
import argparse
from conf.settings import logger



ip_list = []

def remote_push():
    parser = argparse.ArgumentParser(add_help=True,description='WafCheckToo')
    parser.add_argument('-I','--install_ec2',help="waf install, example : {-I test_waf}")
    parser.add_argument('-c','--check_install_results',help="check install result")
    parser.add_argument('-a','--add_crontab',action="store_true",help="add_crontab example: {-a}")
    parser.add_argument('-S','--add_reboot_crontab',action="store_true",help="add_reboot_crontab example: {-S}")
    parser.add_argument('-r','--reboot_server',action="store_true",help="reboot server")

    obj = parser.parse_args()
    ED = ExecuteDeploy()
    if obj.install_ec2:
        post_params = "-I {}".format(obj.install_ec2)
        ED.split_execute(ip_list,post_params)
    elif obj.check_install_results:
        task_id = obj.check_install_results.split(',')
        ED.echo_deploy_status(task_id)
    elif obj.add_crontab:
        post_params = "-a"
        ED.split_execute(ip_list,post_params)
    elif obj.add_reboot_crontab:
        post_params = "-S"
        ED.split_execute(ip_list,post_params)
    elif obj.reboot_server:
        post_params = "-r"
        ED.split_execute(ip_list,post_params)
    else:
        print('example -h')
        exit(1)

if __name__ == '__main__':
    remote_push()
