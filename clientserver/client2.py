#!/usr/bin/python3

import click
import socket
import sys
import threading
import signal

'''

connection handled
client chat messages processed
joining and leaving messages processed
keep alive processed
client or server shutdown handled 
the list of chat room member processed
easy to follow program logic
interoperates with other student implementations

'''


@click.command()
@click.argument('name')
@click.argument('host')  # IP Address
@click.argument('port', type=click.INT)
def do_client(name, host, port): # main
    print("opening connection to {}:{}".format(host, port))
    # TCP socket
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server
    sd.connect((host, port))
    print("Connected\n")
    # get user name, send to server
    # print("Get user name: "+name)
    name = name + "\n"
    sd.send(name.encode())
    # print("Name sent\n")
    try:
        # print("thread0")
        threading.Thread(target=send_mesg,args=(sd,)).start()
        # print("thread1")
        threading.Thread(target=receive_mesg,args=(sd,)).start()
        # print("thread2")
        threading.Timer(15.0, send_alive_Mesg,args=[sd,]).start()
        # print("thread3")
    except Exception:
        print("get exception do client")


# thread
def send_mesg(_socket):
    # ===== same thing above=====
    # data from client to server
    # mess: message\n, alive:\n, whoisthere:\n
    try:
        while True:
            print("Enter mesg: \n")
            user_mesg = sys.stdin.readline()  # use input()?
            if(user_mesg != "\n"): # when user enter something, send to server, otherwise, do not send anything
                encoded_mesg = encode_mesg(user_mesg)
                _socket.send(encoded_mesg.encode())
    except ConnectionResetError:
         print("Server is closed")
    except ConnectionAbortedError:
         print('Server closed this connection!')
    except Exception:
        print("get an exception-send")
        _socket.close()
        exit()
        # break


# thread
def receive_mesg(_socket):
    # mesg from server to client
    try:
        while True:
            server_mesg = _socket.recv(2048)
            if not server_mesg:
                raise Exception # when no message come from server, break & stop
            else:
                decoded_mesg = decode_mesg(server_mesg.decode(),_socket)
                print(decoded_mesg)
    except ConnectionResetError:
        print("Server is closed")
    except ConnectionAbortedError:
        print('Server closed this connection!')
    except:
        print("get an exception-receive")
        _socket.close()
        exit()
        # break


# thread
def send_alive_Mesg(_socket):
    try:
        _socket.send(b"alive:\n")
        # print("alive sent")
    except ConnectionResetError:
        print("Server is closed")
    except ConnectionAbortedError:
        print('Server closed this connection!')
    except Exception:
        print("get an exception-receive")
        # _socket.close()
        sys.exit()

    threading.Timer(15.0, send_alive_Mesg, args=[_socket, ]).start()


def encode_mesg(_mesg):
    if _mesg == "/list\n":  # check whoisthere:
        #print("encode1")
        return "whoisthere:\n"  # return to the current alive user list
    else:
        #print("encode2")
        return "mess: "+_mesg # careful on \n


def decode_mesg(_mesg,_socket):
        # possible messages from server
        # joined: name\n, left: name\n, present: name\n, mess-name: message\n, alive:\n

        if _mesg[0:4] == "mess":
            return _mesg[5:]  # mesg from other clients

        elif _mesg[0:4] == "join":
            return _mesg[8:] + " joined\n"

        elif _mesg[0:4] == "left":
            return _mesg[6:] + " left\n"

        elif _mesg[0:4] == "pres":
            return _mesg

        elif _mesg[0:4] == "aliv":
            return "alive:\n"


if __name__ == "__main__":
    try:
        do_client()
    except KeyboardInterrupt:
        print("keyboardInterrupt get")
        raise
    except Exception:
        print("stop program 0")
        sys.exit()
