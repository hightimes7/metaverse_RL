import threading
import socket
import time


isRunning = True

def work1(sock):
    global isRunning
    while isRunning:
        try:
            data = sock.recv(1024)
            if data == None or len(data) <= 0:
                print('E1')
                isRunning = False
                return
        except socket.error:
            print('E2')
            isRunning = False
            return
        sdata = data[4:].decode()
        ss = sdata.split()
        if ss[0] == 'update':
            for r in range(8):
                print('+---'*8+'+')
                for c in range(8):
                    if ss[2][r*8+c] == '0':
                        print(f'|{r*8+c:^3}', end='')
                    elif ss[2][r*8+c] == '3':
                        print('|   ', end='')
                    elif ss[2][r*8+c] == '1':
                        print('| 0 ', end='')
                    elif ss[2][r*8+c] == '2':
                        print('| X ', end='')
                print('|')
            print('+---'*8+'+')
        else:
            print(sdata)

def work2(sock):
    global isRunning
    while isRunning:
        s = input('>> ')
        if s == '/quit':
            isRunning = False
            return
        data = s.encode()
        packet = ('%04d'%len(data)).encode()+data
        sock.send(packet)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect( ('127.0.0.1', 8888) )
except socket.error:
    print(f'Network error {socket.error}')
    quit()

print('Connection is established')
thread1 = threading.Thread(target=work1, args=(sock,))
thread1.start()
thread2 = threading.Thread(target=work2, args=(sock,))
thread2.start()
thread1.join()
thread2.join()
