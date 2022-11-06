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

class Client:
    def __init__(self, serverIP='localhost', user='joao', serverPort=12000, cert=None):
        self.sock = socket(AF_INET, SOCK_STREAM, 0)
        self.user = user
        self.serverIP=serverIP
        self.serverPort=serverPort
        if cert:
            self.set_sslcontext(cert=cert)
            console.print('\n')
            console.rule(f'[bold green]🔒 Secure client created at: [bold white] {serverIP}:{serverPort}')

        else:
            self.ssock=False
            console.print('\n')
            console.rule(f'[bold red]🔓 Insecure client created at: [bold white] {serverIP}:{serverPort}')
        self.connect()

    def set_sslcontext(self, cert=None):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(cert)
        self.ssock = context.wrap_socket(self.sock, server_hostname=self.serverIP)

    def connect(self):
        if self.ssock:
            self.ssock.connect((self.serverIP, self.serverPort))
            self.conn=self.ssock
        else:
            self.conn=self.sock.connect((self.serverIP, self.serverPort))
            self.conn=self.sock
        self.receive()

    def handle_rcv(self, conn):
        while True:
            message = json.loads(conn.recv(1024).decode('utf-8'))
            user = message['user']
            if user!=self.user:
                print_message(message)
            else:
                print_my_message(message)

    def receive(self):
        self.receive_thread = threading.Thread(target=self.handle_rcv, args=(self.conn,)) 
        self.receive_thread.start()

    def send(self, content, destination):
        self.conn.send(
                json.dumps(
                    {
                        'user':self.user,
                        'content':content,
                        'destination':destination
                    }
                ).encode('utf-8')
            )


@click.group()
def app():
    """Chat Client."""

@app.command(name="run")
@click.option("--user", default='joao', help="Chat User")
@click.option("--certBundle", default='cert.pem', help="Certificate Bundle")
@click.option("--serverIP", default='localhost', help="Server IP")
@click.option("--serverPort", default=12000, help="Server Port")
def main(user, certbundle, serverip, serverport):
    """Run Client."""
    cli = Client(serverIP=serverip, user=user, serverPort=serverport, cert=certbundle)
    while True:
        content = input()
        destination = Prompt.ask("Destination", choices=["Paul", "Jessica", "Duncan"], default="All")

        cli.send(content, destination)
if __name__=='__main__':
    app()