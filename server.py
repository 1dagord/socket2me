"""
	TODO:
		- create aliases/usernames to make connecting easier
		- allow users to change username and password
		- use TCP instead of UDP
"""

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class Server(DatagramProtocol):
	def __init__(self):
		self.clients = set()
		self.encoding = "utf-8"

	def datagramReceived(self, datagram: bytes, addr: int) -> None:
		datagram = datagram.decode(self.encoding)
		addresses = "\n".join([str(x) for x in self.clients])

		if datagram == "ACK":
			self.transport.write(addresses.encode(self.encoding), addr)
			self.clients.add(addr)


if __name__ == "__main__":
	port = 52002
	reactor.listenUDP(port, Server())
	reactor.run()
