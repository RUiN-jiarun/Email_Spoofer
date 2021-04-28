#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An e-mail sender implemented by SMTP
"""

from socket import *
import time
import ssl
import base64
from io import StringIO 
from time import gmtime, strftime
import random
import string
import dns.resolver
import dkim
import traceback

def get_date():
	mdate= strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
	return (mdate).encode("utf-8")

def id_generator(size=6):
	chars=string.ascii_uppercase + string.digits
	return (''.join(random.choice(chars) for _ in range(size))).encode('utf-8')

def generate_dkim_header(dkim_msg, dkim_para):
	d = dkim.DKIM(dkim_msg)
	dkim_header = d.sign(dkim_para['s'], dkim_para['d'], open('key.pem','rb').read(), canonicalize=(b'simple',b'relaxed'), include_headers=[b'from']).strip()+b'\r\n'
	return dkim_header

class MailSender(object):
	def __init__(self):
		self.sending_server = ""
		self.sender_addr = ""
		self.password = ""

		self.rcpt_to = ""
		self. helo = ""
		self.mail_from = ""

		self.dkim = ""

		self.data = ""
		self.msg = ""

		self.starttls = False		# Support TLS or not
		self.client_socket = None
		self.tls_socket = None


	def set_param(self, sender_addr, password, rcpt_to, helo, 
				mail_from, dkim_para, starttls, Subject, From, body):
		self.sender_addr = sender_addr.encode()
		if password is not None:
			self.password = password.encode()
			self.sending_server = ('smtp.' + sender_addr[(sender_addr.index('@')+1):], 25)
		else:
			self.password = None
			self.sending_server = (sender_addr, 25)

		if dkim_para is not None:
			dkim_msg = dkim_para['sign_header'] + b'\r\n\r\n' + body.encode()
			dkim_header = generate_dkim_header(dkim_msg, dkim_para)
			self.dkim = dkim_header
		else:
			self.dkim = None

		self.rcpt_to = rcpt_to.encode()
		self.mail_from = mail_from.encode()
		self.helo = helo.encode()
		
		self.starttls = starttls
		self.data = {
			"from_header": b"From: " + From + b"\r\n",
            "to_header": b"To: " + rcpt_to.encode() + b"\r\n",
            "subject_header": b"Subject:" + Subject.encode() + b"\r\n",
            "body": body.encode() + b"\r\n",
            "other_headers": b"Date: " + get_date() + b"\r\n" + b'Content-Type: text/plain; charset="UTF-8"\r\nMIME-Version: 1.0\r\nMessage-ID: <1538085644648.096e3d4e-bc38-4027-b57e-' + id_generator() + b'@spoof.com>\r\nX-Email-Client: https://github.com/RUiN-jiarun\r\n\r\n',
		}

		if self.dkim is not None:
			self.msg = self.data["from_header"] + self.dkim + self.data["to_header"] + self.data["subject_header"] + self.data["other_headers"] + self.data["body"]
		else:
			self.msg = self.data["from_header"] + self.data["to_header"] + self.data["subject_header"] + self.data["other_headers"] + self.data["body"]

	def establish_socket(self):
		client_socket = socket(AF_INET, SOCK_STREAM)
		print("Connecting "+ str(self.sending_server))
		client_socket.connect(self.sending_server)
		self.print_recv_msg(client_socket)

		if self.starttls == True:
			client_socket.send(b"ehlo "+ self.helo +b"\r\n")
			self.print_send_msg("ehlo "+ self.helo.decode("utf-8")+"\r\n")
			self.print_recv_msg(client_socket)

			client_socket.send(b"starttls\r\n")
			self.print_send_msg("starttls\r\n") 
			self.print_recv_msg(client_socket)

			tls_socket = ssl.wrap_socket(client_socket, ssl_version=ssl.PROTOCOL_TLS)
			self.tls_socket = tls_socket

		self.client_socket = client_socket

	def send_smtp_cmds(self, client_socket):
		client_socket.send(b"ehlo "+self.helo+b"\r\n")
		time.sleep(0.1)
		self.print_send_msg("ehlo "+ self.helo.decode("utf-8")+"\r\n") 
		recv_msg = self.print_recv_msg(client_socket)

		if self.password != None:
			if "LOGIN".lower() in recv_msg.lower():
				auth_username = b"AUTH LOGIN " + base64.b64encode(self.sender_addr) + b"\r\n"
				client_socket.send(auth_username)
				self.print_send_msg(auth_username.decode("utf-8"))
				self.print_recv_msg(client_socket)
		
				auth_pwd = base64.b64encode(self.password) + b"\r\n"
				client_socket.send(auth_pwd)
				self.print_send_msg(auth_pwd.decode("utf-8"))
				self.print_recv_msg(client_socket)
			else:
				auth_msg = b'AUTH PLAIN '+base64.b64encode(b'\x00'+ auth_username+b'\x00'+self.password)+b'\r\n'
				client_socket.send(auth_msg)
				self.print_send_msg(auth_msg.decode("utf-8"))
				self.print_recv_msg(client_socket)


		client_socket.send(b'mail from: '+ self.mail_from + b'\r\n')
		time.sleep(0.1)
		self.print_send_msg('mail from: '+ self.mail_from.decode("utf-8") + '\r\n')
		self.print_recv_msg(client_socket)

		client_socket.send(b"rcpt to: "+ self.rcpt_to+ b"\r\n")
		time.sleep(0.1)
		self.print_send_msg("rcpt to: " + self.rcpt_to.decode("utf-8") + "\r\n")
		self.print_recv_msg(client_socket)

		client_socket.send(b"data\r\n")
		time.sleep(0.1)
		self.print_send_msg( "data\r\n")
		self.print_recv_msg(client_socket)

		client_socket.send(self.msg+b"\r\n.\r\n")
		time.sleep(0.1)
		self.print_send_msg(self.msg.decode("utf-8")+"\r\n.\r\n")
		self.print_recv_msg(client_socket)

	def send_quit_cmd(self, client_socket):
		client_socket.send(b"quit\r\n")
		self.print_send_msg( "quit\r\n")
		self.print_recv_msg(client_socket)

	def close_socket(self):
		if self.tls_socket != None:
			self.tls_socket.close()
		if self.client_socket != None:
			self.client_socket.close()

	def read_line(self, sock):
		buff = StringIO()
		while True:
			data = (sock.recv(1)).decode("utf-8")
			buff.write(data)
			if '\n' in data: break
		return buff.getvalue().splitlines()[0]

	def print_send_msg(self, msg):
		print("<<< " + msg)

	def print_recv_msg(self, client_socket):
		print(">>> ", end='')
		time.sleep(1)
		time.time()

		msg = ""
		while True:
			line  = self.read_line(client_socket)
			msg += line
			print(line) 
			if "-" not in line:
				break
			else:
				if len(line) > 5 and "-" not in line[:5]:
					break
			time.sleep(0.1)
		return msg

	def send_email(self):
		self.establish_socket()
		try:
			if self.starttls == True:
				self.send_smtp_cmds(self.tls_socket)
				self.send_quit_cmd(self.tls_socket)
			else:
				self.send_smtp_cmds(self.client_socket)
				self.send_quit_cmd(self.client_socket)
			self.close_socket()
		except Exception:
			traceback.print_exc()	

	def __del__(self):
		self.close_socket()
