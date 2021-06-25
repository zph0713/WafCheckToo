import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from urllib.parse import urljoin
from common import logs

#imperva info#
imperva_user = 'admin'
imperva_password = ''



## config path##
confDir = os.path.join(BASEDIR,'conf')
logDir = os.path.join(BASEDIR,'logs')
templateDir = os.path.join(BASEDIR,'template')
scriptsDir = os.path.join(BASEDIR,'scripts')

main_config = os.path.join(confDir,'main_config.json')
gateway_config = os.path.join(confDir,'gateway_config.json')
mx_config = os.path.join(confDir,'mx_config.json')
haproxy_config = os.path.join(confDir,'haproxy_default_config.json')

gateway_template = os.path.join(templateDir,'gateway_template')
mx_template = os.path.join(templateDir,'mx_template')

haproxy_main_conf_template = os.path.join(templateDir,'haproxy_main_conf_template')
haproxy_listen_conf_template = os.path.join(templateDir,'haproxy_listen_conf_template')
haproxy_ng_conf_template = os.path.join(templateDir,'haproxy_ng_conf_template')

final_config_path = os.path.join(confDir,'haproxy.cfg')
haproxy_config_path = "/etc/haproxy/"
current_config_path = os.path.join(haproxy_config_path,'haproxy.cfg')
backup_config_path = os.path.join(confDir,'haproxy.cfg.backup')
script_path = "/lingtian/shell/"
##other##
install_command_path = "/opt/SecureSphere/etc/ec2/"
imperva_ctl_command = "impctl"


##logs info##
log_file_name = 'wafchecktoo_install'+'.log'
log_file = os.path.join(logDir,log_file_name)
logger = logs.Log("WafCheckToo", console=1, logfile=log_file, show_details=True)
logger.set_debug_level()
