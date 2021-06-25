import __init__
from core.waf_status_check import WafCheck
from core.install_push import ExecuteDeploy
import argparse
from conf.settings import logger


def war_manager():
    parser = argparse.ArgumentParser(add_help=True,description='WafCheckToo')
    parser.add_argument('-C','--waf_check',action="store_true",help="waf check")

    obj = parser.parse_args()
    if obj.waf_check:
        WC = WafCheck()
        WC.analysis_coverage()
    else:
        print('example -h')
        exit(1)

if __name__ == '__main__':
    war_manager()
