from rich.console import Console
from rich.panel import Panel, Text
from rich.prompt import Prompt


console = Console()

def print_message(message):
    console.print(Panel(Text(message['content'], justify="left"), subtitle=f'{message["user"]}|{message["origin"]}', subtitle_align='right', width=50), justify="right")

def print_my_message(message):
    console.print(Panel(Text(message['content'], justify="left"), subtitle='[cyan]You', subtitle_align='left', width=50), justify="left")
