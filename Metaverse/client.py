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
                isRunning = False
                return
        except socket.error:
            isRunning = False
            return
        sdata = data.decode()
        print(sdata)

def work2(sock):
    global isRunning
    while isRunning:
        s = input('>> ')
        if s == '/quit':
            isRunning = False
            return
        sock.send(s.encode())

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

#isRunning = False
#thread.join()
