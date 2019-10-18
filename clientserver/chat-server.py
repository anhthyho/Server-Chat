import sys

import click
import socket
from threading import Thread
import time

from pip._vendor.distlib.compat import raw_input


class ClientThread (Thread):

    def __init__(self, sd):
        self.sd = sd

    def run(self):
        name = ""
        clients.add(self)
        while True:
            try:
                data = self.sd.recv(1024)
                if not data:
                    break
                dstring = data.decode()
                if dstring[:6] == 'alive:':
                    print("received alive msg")
                    data = "alive"
                    broadcast(data.encode())
                elif dstring[6: 16] == 'whoisthere':
                    for name in names:
                        data = "present: " + name + "\n"
                        broadcast(data.encode())

                elif (dstring[:4] != 'mess') & (len(name) == 0):
                    name = dstring.split('\n', 1)[0]
                    names.append(name)

                    print(name + " has joined serverside")

                    data = "joined: " + name
                    broadcast(data.encode())
                else:
                    #print("mess-" + name + ":" + dstring[5:])

                    data = "mess-" + name + ":" + dstring[5:]
                    broadcast(data.encode())
            except ConnectionResetError:
                data = ("left: " + name)
                print(data)
                broadcast(data.encode())
                break
        self.sd.close()
        clients.remove(self)

    def send(self, data):
        self.sd.sendall(data)

names = set()
clients = set()
def broadcast(data):
    for client in clients:
        client.send(data)

def keep_alive(sock):

    for client in clients:
        data = 'are you there?'
        client.send(data.encode())
    # https://stackoverflow.com/questions/12248132/how-to-change-tcp-keepalive-timer-using-python-script
    # enable sock keep alie, 30 sec keep alive time, 15 second keep alive interval
    sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 30000, 15000))


@click.command()
@click.argument('port', type=click.INT)
def do_server(port):
    'simple program to listen on a socket and start a thread'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as ld:
        ld.bind(("", port))
        ld.listen(10)
        while True:
            try:
                (sd, addr) = ld.accept()
                keep_alive(ld)
                ct = ClientThread(sd)
                clients.add(ct)
                ct.run()
            except ConnectionResetError:
                ("gone!")
        sd.close()


if __name__ == '__main__':
    do_server()
