#!/usr/bin/python3
"""
	sprayette.py protocol ip user pass attemps timer 
					port optional
"""

import argparse
import time
import telnetlib
import paramiko
import os

#variables
user_list = list()
pass_list = list()
#ports
spec_port=None
smb_p=139

def pGreen(value): return '\033[92m{}\033[90m'.format(value)
def pRed(value): return ''.format(value)
def pWarning(value): return '\033[93m{}\033[90m'.format(value)

parser = argparse.ArgumentParser()
parser.add_argument('protocol', type=str,help='Protocol to perform the spray (telnet,ssh,ftp,smb)')
parser.add_argument('ip', type=int,help='The ip to perform the spray')
parser.add_argument('-p','--port',type=int, default=False,dest='spec_port')
parser.add_argument('users',help='Users list (one per line)')
parser.add_argument('pass', help='Passwords list (one per line)')
parser.add_argument('attemps', type=int,help='The amount of attemps before the timer starts')
parser.add_argument('timer', type=int,help='The sleep time (minutes)')
args = parser.parse_args()
ip = args.ip
prot = args.protocol
c_attemps = args.attemps
timer = args.timer*60 #secods


def ftp_connect(ip,user,password):
	return
def telnet_connect(ip,user,password):
	return
def ssh_connect(ip,user,password):
	return
def smb_connect(ip,user,password):
	return

def spray():
	with 
	return

if __name__ == '__main__':
	spray()