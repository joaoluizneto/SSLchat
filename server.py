from socket import *
import ssl
import threading
from random import randint
from console import *
import json
import click

console.print(Panel("""[bold red]
 
 ______   ______     ______     __    __    
/\__  _\ /\  ___\   /\  == \   /\ "-./  \   
\/_/\ \/ \ \  __\   \ \  __<   \ \ \-./\ \  
   \ \_\  \ \_____\  \ \_\ \_\  \ \_\ \ \_\ 
    \/_/   \/_____/   \/_/ /_/   \/_/  \/_/ 
                                            
 ______     __  __     ______     ______    
/\  ___\   /\ \_\ \   /\  __ \   /\__  _\   
\ \ \____  \ \  __ \  \ \  __ \  \/_/\ \/   
 \ \_____\  \ \_\ \_\  \ \_\ \_\    \ \_\   
  \/_____/   \/_/\/_/   \/_/\/_/     \/_/   
                                            
                                                                                                         
""", subtitle='Developed by joaoluizneto', subtitle_align='right', title='Welcome to', title_align='left', width=50), justify='center')


class Server:
    def __init__(self, serverIP='localhost', serverPort=12000, cli_num=5, key=None, cert=None):
        self.clientDict = {}
        self.sock = socket(AF_INET, SOCK_STREAM, 0)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((serverIP, serverPort))
        self.sock.listen(cli_num)

        if key:
            self.set_sslcontext(key=key, cert=cert)
            console.print('\n')
            console.rule(f'[bold green]🔒 Secure Server created at:[bold white] {serverIP}:{serverPort}')

        else:
            self.ssock=False
            console.rule(f'[bold red]🔓 Insecure Server created at:[bold white] {serverIP}:{serverPort}')


    def set_sslcontext(self, key=None, cert=None):
        self.sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.sslcontext.load_cert_chain(cert, key)
        self.ssock = self.sslcontext.wrap_socket(self.sock, server_side=True)

    def handle_rcv(self, conn, addr):
        console.print('Captando mensagens de [bold green]', addr)
        while True:
            console.print(f"Waiting for messages from {addr}...")
            rcvd = conn.recv(1024).decode('utf-8')
            console.print(rcvd)
            message = json.loads(rcvd)
            message['origin']=addr
            self.clientDict[addr]['user']=message['user']
            console.print(f'received message from {addr}, fowarding to {message["destination"]}.')
            self.foward(message)

    def receive(self):
        while True:
            if self.ssock:
                conn, addr = self.ssock.accept()
            else:
                conn, addr = self.sock.accept()
            
            thr = threading.Thread(target=self.handle_rcv, args=(conn,addr)) 

            self.clientDict[addr] = {
                "conn":conn,
                "thr":thr,
                'user':None
            }
            thr.start()

    def foward(self, message):
        if message['destination'] in [self.clientDict[addr]["user"] for addr in self.clientDict]:
            conn = [self.clientDict[addr]['conn'] for addr in self.clientDict][0]
            conn.send(json.dumps(message).encode('utf-8'))
            print("SPECIFIC")
        else:
            for addr in self.clientDict:
                self.clientDict[addr]["conn"].send(json.dumps(message).encode('utf-8'))
                print("NOT SPECIFIC")


@click.group()
def app():
    """Chat Server."""

@app.command(name="run")
@click.option("--numCli", default=5, help="Limit number of clients")
@click.option("--key", default='key.pem', help="Private Key")
@click.option("--cert", default='cert.pem', help="Self Signed Certificate")
@click.option("--serverIP", default='localhost', help="Server IP")
@click.option("--serverPort", default=12000, help="Server Port")
def main(numcli, key, cert, serverip, serverport):
    """Run Server."""
    serv = Server(serverIP=serverip, serverPort=serverport, cli_num=numcli, key=key, cert=cert)
    serv.receive()

if __name__=='__main__':
    app()