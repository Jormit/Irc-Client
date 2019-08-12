import socket
import time
import threading
import os
import re


class Irc:
	socket = socket.socket()

	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self, server, port, nick, password, channel):
		print("Connecting to: " + server)
		self.socket.connect((server,port))

		self.socket.send(bytes("USER " + nick + " " + nick +" " + nick + " :python\n", "UTF-8"))
		self.socket.send(bytes("NICK " + nick + "\n", "UTF-8"))
		self.socket.send(bytes("NICKSERV IDENTIFY " + password + " " + password + "\n", "UTF-8"))
		time.sleep(5)

		self.socket.send(bytes("JOIN " + channel + "\n", "UTF-8"))

	def response(self):		
		time.sleep(1)
		resp = self.socket.recv(2040).decode("UTF-8")

		return resp


	def send(self,message,channel):
		irc.socket.send(bytes("PRIVMSG " + channel + " " + message + "\n", "UTF-8"))

def get_input(irc):
	while True:
		message = input()
		if (message == "exit"):
			os._exit(1)
		irc.send(message,"#main")
		

irc = Irc()

irc.connect("chat.freenode.net", 6667, "jjjjjjj", "password", "#main")

response_thread = threading.Thread(target=get_input, args=(irc,))
response_thread.start()

while True:
	resp = irc.response()
	print(resp)





