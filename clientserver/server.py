import click
import socket
from threading import Thread
import time

from pip._vendor.distlib.compat import raw_input


class ClientThread (Thread):
    def __init__(self, sd):
        self.sd = sd
        Thread.__init__(self)
        print("new server socket thread")

    def run(self):
        while True:
            data = self.sd.recv(1024)
            name = ""
            if not data:
                break
            dstring = data.decode()
            if dstring[:2] == 'gb':
                print("bye")
                self.sd.close()
            elif dstring[:6] == 'alive:':
                print("i'm dead inside")
            elif dstring[:11] == 'whoisthere':
                print("ur mum")
            elif dstring[:5] != 'name\n':
                names.append(dstring)
                print("name is: " + dstring)
                broadcast(data)
            else:
                print("k")
                broadcast(data)
        self.sd.close()
        clients.remove(self)

    def send(self, data):
        self.sd.sendall(data)

names = []
clients = set()
def broadcast(data):
    for client in clients:
        client.send(data)


@click.command()
@click.argument('port', type=click.INT)
def do_server(port):
    'simple program to listen on a socket and start a thread'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as ld:
        ld.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 15)
        ld.bind(("", port))
        ld.listen(10)
        while True:
            (sd, addr) = ld.accept()
            ct = ClientThread(sd)
            clients.add(ct)
            ct.run()

if __name__ == '__main__':
    do_server()
