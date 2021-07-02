import __init__
from prettytable import PrettyTable
from conf import settings
from conf.settings import logger


def config_viewer(config_path):
    with open(config_path,'r') as target:
        print(target.read())

def check_waf_coverage(check_results):
    data_table = PrettyTable(['count','website','event_id','waf_enable'])
    count = 0
    for data in check_results:
        count+=1
        data_table.add_row([count,data['website'],data['event_id'],data['waf_enable']])
    logger.info(data_table)
    return data_table



if __name__ == "__main__":
    data_tansfer_markdown()
