#!/usr/bin/python3
# reference notes
# break if/else from geeksforgeeks socket p. with multi-threading in python
import click
import socket



@click.command()
@click.argument('name')
@click.argument('host')
@click.argument('port', type=click.INT)
def do_client(name, host, port):
    print("opening connection to {}:{}".format(host, port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sd:
        sd.connect((host, port))
        while True:

            message = input(" -> ")  # take input
            while True:
                sd.send(message.encode())
                data = sd.recv(1024).decode()

                print(repr(data))
                message = input(" -> ")
                if message == 'gb':
                    print("goodbye!")
                    sd.close()  # close connectionc
                    break
                else:
                    continue
            sd.close()  # close connectionc




if __name__ == "__main__":
    do_client()
