import socket
import time
import threading
import os
from datetime import datetime
import sys

# Class handles all irc i/o.
class Irc:
	socket = socket.socket()

	def __init__(self,  username, password, server = "irc.freenode.net", port = 6667):
		self.username = username
		self.server = server
		self.port = int(port)
		self.channel = ""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.password = password

	def connect(self):
		print("Connecting to: " + self.server)
		self.socket.connect((self.server,self.port))

		self.socket.send(bytes("USER " + self.username + " " + self.username +" " + self.username + " :python\n", "UTF-8"))
		self.socket.send(bytes("NICK " + self.username + "\n", "UTF-8"))
		self.socket.send(bytes("NICKSERV IDENTIFY " + self.username + " " + self.password + "\n", "UTF-8"))
		time.sleep(5)

		#self.socket.send(bytes("JOIN " + self.channel + "\n", "UTF-8"))

	def response(self):		
		time.sleep(1)
		resp = self.socket.recv(2040).decode("UTF-8")

		if resp.find('PING') != -1:                      
			self.socket.send(bytes('PONG ' + resp.split()[1] + '\r\n', "UTF-8")) 

		return resp

	def print_response(self):
		resp = self.response()
		if resp:
			try:
				msg = resp.split(":")
				print(datetime.now().strftime('%d %H:%M:%S') + " <" + msg[1].split("!")[0] + "> " + msg[2].strip())
			except:
				print(resp)

	def send(self,message):
		irc.socket.send(bytes("PRIVMSG " + self.channel + " :"  + message + "\n", "UTF-8"))
	
	def handle_command(self, message):
		if (message.startswith("/join")):
			try:
				self.channel = message.split()[1]
				self.socket.send(bytes("JOIN " + self.channel + "\n", "UTF-8"))
			except:
				pass
		if (message.startswith("/q")):
			os._exit(1)
		if (message.startswith("/names")):
			try:
				self.socket.send(bytes("NAMES " + self.channel + "\n", "UTF-8"))
			except:
				pass

def get_input(irc):
	while True:
		message = input()

		if (message.startswith("/")):
			irc.handle_command(message)
			continue

		irc.send(message)
		print(datetime.now().strftime('%d %H:%M:%S') + " <" + irc.username + "> " + message)


if (len(sys.argv) < 3):
	print("You need to specify the server to connect to:")
	print("python main.py server.net 3333")
	exit(1)

username = input("Enter username: ")
password = input("Enter password: ")

irc = Irc(username, password, sys.argv[1], sys.argv[2])

irc.connect()

# Start the input thread.
response_thread = threading.Thread(target=get_input, args=(irc,))
response_thread.start()

# Start the response loop.
while True:
	irc.print_response()