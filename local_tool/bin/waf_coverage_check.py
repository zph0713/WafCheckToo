import __init__
from core.waf_status_check import WafCheck
from core.install_push import ExecuteDeploy
from core.slack_format import CoverageSlackFormat
from common.slacks import SlackSender
import argparse
from conf.settings import logger


def war_manager():
    parser = argparse.ArgumentParser(add_help=True,description='WafCheckToo')
    parser.add_argument('-C','--waf_check',action="store_true",help="waf check")

    obj = parser.parse_args()
    if obj.waf_check:
        WC = WafCheck()
        waf_check_results,coverage,ab_public_domain = WC.analysis_coverage()
        CSF = CoverageSlackFormat(waf_check_results,coverage,ab_public_domain)
        msg = CSF.create_waf_coverage_block()
        SS = SlackSender()
        SS.send_msg(msg)
    else:
        print('example -h')
        exit(1)

if __name__ == '__main__':
    war_manager()
