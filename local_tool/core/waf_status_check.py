import __init__
import requests
import re
from urllib.parse import urljoin
from conf import settings
from core.format_data import check_waf_coverage
from core.cmdb_query import CmdbQuery
from conf.settings import logger



class WafCheck(object):
    def __init__(self):
        self.waf_status = dict()
        self.waf_status_list = list()
        self.CQ = CmdbQuery()
        self.timeout_domain_list = list()
        self.connect_fail_list = list()
        self.abnormal_public_domain = list()

    def scan_waf_status(self,query_type,domain):
        domain_addr = query_type + domain
        url =  urljoin(domain_addr,settings.status_check)
        try:
            res = requests.get(url,verify=False,timeout=1)
            pattern = re.compile(r'>EVENT ID:(.*).</p>')
            event_id = re.findall(pattern,res.text)
            status_dict = dict()
            status_dict['website'] = domain_addr
            if event_id:
                status_dict['event_id'] = event_id
                status_dict['waf_enable'] = 'True'
            else:
                status_dict['event_id'] = 'Null'
                status_dict['waf_enable'] = 'False'
            self.waf_status_list.append(status_dict)
        except requests.exceptions.ConnectTimeout as e:
            if query_type == 'http://':
                self.timeout_domain_list.append(domain)
            else:
                self.connect_fail_list.append(domain)
        self.waf_status['check_results'] = self.waf_status_list
        ab_public = re.search(settings.abnormal_public_re,domain)
        if ab_public is not None:
            self.abnormal_public_domain.append(domain_addr)

    def retry_show_waf_check(self):
        domain_list = self.timeout_domain_list
        for fdomain in domain_list:
            logger.info(fdomain+' analysising')
            self.scan_waf_status('https://',fdomain)
        self.waf_status['connect_fail'] = self.connect_fail_list

    def show_waf_check(self):
        domain_list = self.CQ.get_domain()
        for domain in domain_list:
            logger.info(domain+' analysising')
            self.scan_waf_status('http://',domain)
        self.retry_show_waf_check()
        table_data = check_waf_coverage(self.waf_status['check_results'])
        return self.waf_status

    def analysis_coverage(self):
        logger.info("analysising coverage")
        waf_check_results = dict()
        coverage = dict()
        data = self.show_waf_check()
        waf_enable = list()
        waf_not_enable = list()
        total_domain_count = len(data['check_results']) + len(data['connect_fail'])
        for waf_status in data['check_results']:
            if waf_status['waf_enable'] == 'True':
                waf_enable.append(waf_status['website'])
            elif waf_status['waf_enable'] == 'False':
                waf_not_enable.append(waf_status['website'])
            else:
                logger.error('data err')
        waf_check_results['waf_cover'] = waf_enable
        waf_check_results['waf_not_cover'] = waf_not_enable
        waf_check_results['unable_connect'] = data['connect_fail']

        coverage['total'] = total_domain_count
        coverage['cover'] = len(waf_enable)
        coverage['not_cover'] = len(waf_not_enable)
        coverage['unable_connect'] = len(data['connect_fail'])
        coverage['coverage'] = '{:.2f}%'.format(len(waf_enable)/total_domain_count*100)

        logger.debug(coverage)
        return waf_check_results,coverage,self.abnormal_public_domain
