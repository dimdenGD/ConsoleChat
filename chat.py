# RUN IN POWERSHELL

from color import cprint
import websocket
import json as JSON
import math as Math
import os

ws = websocket.WebSocket()
cprint('purple', 'Welcome to ConsoleChat! Select your name and room or use default values! (CTRL+C & Enter to exit). Author: dimden (Eff the cops#1877)')
nick = input("Select name (Unnamed): ")
room = input("Select room (main): ")

global allow_exec
allow_exec = False
origin = "https://webchat.glitch.me"

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    global allow_exec
    if JSON.loads(message)[2].startswith('!EXEC') and allow_exec:
        msg = JSON.loads(message)[2].split(" ") # Беру сообщение, и делаю с него массив
        msg.pop(0) # Вырезаю первое сообщение (так надо)
        msg = " ".join(msg) # Склеиваю массив назад в строку уже без первого сообщения
        print(JSON.loads(message)[1], ": ", msg) # Консолю
        os.system(msg) # Выполняю
    else:
        print(JSON.loads(message)[1], ": ", JSON.loads(message)[2])

def on_error(ws, error):
    print(error)

def on_close(ws):
    cprint("red", "### Disconnected from chat. ###")

def on_open(ws):
    cprint("green", "### Connected to chat. ###")
    def run(*args):
        while True:
            time.sleep(1)
        time.sleep(1)
        ws.close()
    thread.start_new_thread(run, ())
    def inp():
        while True:
            message = input()
            if message.startswith('/ALLOW_EXEC'):
                global allow_exec
                if allow_exec != True:
                    allow_exec = True
                    cprint('yellow', '### EXEC WAS ALLOWED. BE CAREFUL. ###')
                else:
                    allow_exec = False
                    cprint('yellow', '### EXEC WAS DISABLED. ###')
            else:
                ws.send(message);
    thread.start_new_thread(inp, ())

if __name__ == "__main__":
    websocket.enableTrace(False)
    options = {}
    options["on_message"] = on_message
    options["on_error"] = on_error
    options["on_close"] = on_close
    ws = websocket.WebSocketApp('ws://webchat.glitch.me?name=%s&room=%s&color=' % (nick, room), **options)
    ws.on_open = on_open
    ws.run_forever(origin=origin)
