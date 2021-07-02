import __init__
import os
import json
import time
import matplotlib.pyplot as plt
import numpy as np
from conf import settings
from common.slacks import SlackSender
from common.current_time import current_time


class CoverageSlackFormat(object):
    def __init__(self,waf_status_list,coverage,ab_public_domain):
        self.waf_status_list = waf_status_list
        self.coverage = coverage
        self.ab_public_domain = ab_public_domain

    def create_waf_coverage_block(self):
        upload_result = self.generator_graph()
        time.sleep(2)
        file_path = os.path.join(settings.templateDir,'waf_coverage.json')
        with open(file_path,'r') as tplt:
            block = json.loads(tplt.read())
            block[1]['elements'][0]['text'] = "*{}* | Sec Team".format(current_time())
            block[3]['text']['text'] = "*Total* :{}\n*Cover* :{},  *Not Cover* :{},  *Unable Connect* :{},\n*Coverage* : {}".format(
                self.coverage['total'],self.coverage['cover'],self.coverage['not_cover'],self.coverage['unable_connect'],self.coverage['coverage'])
            block[3]['accessory']['image_url'] = upload_result['file']['url_private']
            block[6]['text']['text'] = self.analysis_ab_public_domain()
            return block

    def analysis_ab_public_domain(self):
        if self.ab_public_domain == []:
            return "public domain normal"
        else:
            text = str()
            for apd in self.ab_public_domain:
                text += "<{}>\n".format(apd)
            return text

    def generator_graph(self):
        data = [self.coverage['cover'],self.coverage['not_cover'],self.coverage['unable_connect']]
        color_list = ['Green','Red','Grey']
        plt.pie(data,labels=['cover','not_cover','unable_connect'],colors=color_list)
        plt.savefig(settings.coverage_pie)
        print('created coverage_pie')
        SS = SlackSender()
        upload_result = SS.upload_file(settings.coverage_pie)
        return upload_result
