import time
import requests
import logging
import sys
import threading
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    DIED = '\033[90m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

logger = logging.getLogger('request')

urls = sys.argv

def color(progress):
	if progress <= 50:
		return bcolors.OKGREEN
	elif progress > 50 and progress < 90:
		return bcolors.WARNING
	elif progress >= 90 and progress < 100:
		return bcolors.FAIL
	else:
		return bcolors.DIED

def proccess():
	print(' '*42 + 'SERVICE MONITORING' + ' '*42)
	print('|%s|' % ('-'*100))
	while True:
		clean = '\033[F\r'
		for i in range(1, len(urls)):
			clean += '\033[F\r\033[F\r'
			sys.stdout.write(bcolors.OKBLUE + '|' + urls[i] + '\n')
			start = time.clock()
			request_time = 0
			try:
				response = requests.get(urls[i], timeout=10)
				request_time = time.clock() - start
			except requests.exceptions.ReadTimeout:
				request_time = 0.1
			except requests.exceptions.ConnectTimeout:
				request_time = 0.1
			if request_time > 0.1:
				request_time = 0.1
			progress = int(float(request_time * 1000))
			print('|%s%s%s%s| %d ns ' % (color(progress), '\033[7m' + ' '*progress + '\033[27m', color(progress), ' '*(100-progress), request_time * 1000000))
		print(bcolors.ENDC + '|%s| \n' % ('-'*100))
		clean += '\033[F\r\033[F\r'
		print(clean)

os.system('clear')
try:
	proccess()
except KeyboardInterrupt:
	os.system('clear')
	sys.exit(1)
