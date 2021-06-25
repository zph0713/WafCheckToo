import __init__
import requests
import rsa
import binascii
from conf import settings
from core.get_token import cmdbToken
from conf.settings import logger




class CmdbQuery(object):
    def __init__(self):
        self.public_ip_list = list()
        self.headers = {'X-Token':cmdbToken()}
        #self.split_pages_query()

    def get_server_count(self):
        logger.debug('get cmdb result count..')
        payload = {'limit':'1'}
        res = requests.get(settings.cmdb_public_ip,params=payload,headers=self.header)
        count = res.json()['data']['count']
        logger.info('cmdbvm results count : {}'.format(count))
        return count

    def split_pages_query(self):
        logger.debug('start split query..')
        count = self.get_server_count()
        pages = count // 1000
        for page in range(0,pages + 1):
            offset_num = page * 1000
            self.get_public_ip(offset_num)

    def rsa_decrypt(self,crypto_ip_list, private_file):
        logger.debug('rsa decrypt')
        public_ip = list()
        with open(private_file, mode='rb') as privatefile:
            private_data = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(private_data)
        for ip in crypto_ip_list:
            message = rsa.decrypt(ip, privkey)
            public_ip.append(message)
        return public_ip


    def get_public_ip(self,offset_num,limit_num=1000):
        logger.debug('get public ip')
        key_path = settings.rsa_key_path
        payload = {'limit':limit_num,'offset':offset_num}
        res = requests.get(settings.cmdb_public_ip,params=payload,headers=self.headers)
        logger.debug(res.url)
        results = res.json()['data']['results']
        for result in results:
            if result['status'] != 'terminated':
                rip = self.rsa_decrypt([binascii.a2b_base64(result['public_ip'])], key_path)[0]
                self.public_ip_list.append(rip)
            else:
                pass
        #print(results)

    def get_domain(self):
        logger.debug('get domain')
        domain_list = list()
        payload = {'domain_type':'public'}
        res = requests.get(settings.cmdb_domain,params=payload,headers=self.headers)
        results = res.json()['data']['results']
        for result in results:
            for record in result['record_list']:
                if record['record_type'] == 'A':
                    #print(result)
                    domain_list.append(result['domain_name'].rstrip('.'))
        domain_list = list(set(domain_list))
        return domain_list
