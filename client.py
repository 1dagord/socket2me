"""
	TODO:
	- print message history above text input area using curses
	- use TCP instead of UDP
"""

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint
import curses


class Client(DatagramProtocol):
	def __init__(self, host, port):
		if host.lower() == "localhost":
			host = "127.0.0.1"

		self.id = (host, port)
		self.address = None
		self.encoding = "utf-8"
		self.server = ("127.0.0.1", 52002)
		print(f"Working on id {self.id}")

	def startProtocol(self):
		self.transport.write("ACK".encode(self.encoding), self.server)

	def datagramReceived(self, datagram, addr):
		datagram = datagram.decode(self.encoding)

		if addr == self.server:
			print("Choose a client\n", datagram)
			self.address = input("Host: "), int(input("Port: "))

			reactor.callInThread(self.send_message)
		else:
			print(f"{addr} : {datagram}")

	def send_message(self):
		while True:
			self.transport.write(input("::: ").encode(self.encoding), self.address)


if __name__ == "__main__":
	port = randint((1 << 12), (1 << 16))
	reactor.listenUDP(port, Client("localhost", port))
	reactor.run()
