import __init__
import json
import re
from conf import settings
from conf.settings import logger



class HaproxyConf(object):
    def __init__(self):
        pass

    def get_config(self,file_path):
        with open(file_path,'r') as target:
            return json.load(target)

    def get_template(self,file_path):
        with open(file_path,'r') as target:
            return target.read()

    def re_tar(self,template):
        logger.info("replace haproxy config template")
        pattern = re.compile(r'@(.*)@')
        rep = re.findall(pattern,template)
        config_data = self.get_config(settings.haproxy_config)
        tar_key = list()
        src_key = '@'+rep[0]+'@'
        for i in rep:
            tar_key.append(config_data[i])
        return src_key,tar_key

    def dump_config_to_file(self,file_text):
        logstext = "dump config to {}".format(settings.final_config_path)
        logger.info(logstext)
        with open(settings.final_config_path,'w') as file:
            file.write(file_text)

    def generator_config(self):
        logger.info("generator haproxy config")
        main_template = self.get_template(settings.haproxy_main_conf_template)
        linsten_template = self.get_template(settings.haproxy_listen_conf_template)
        ng_template = self.get_template(settings.haproxy_ng_conf_template)
        m_src_key,m_tar_key = self.re_tar(main_template)
        for i in m_tar_key:
            main_template = main_template.replace(m_src_key,i)
        l_src_key,l_tar_key = self.re_tar(linsten_template)
        listen_conf = str()
        for r in l_tar_key[0]:
            listen_conf += linsten_template.replace(l_src_key,r)
            n_src_key,n_tar_key = self.re_tar(ng_template)
            for m in n_tar_key[0]:
                listen_conf += ng_template.replace(n_src_key,m)
        final_config = main_template + listen_conf
        self.dump_config_to_file(final_config)
        #return final_config
