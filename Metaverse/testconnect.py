import socket  # use socket module (for network communication)

# make a socket
# AF_INET : internet family
# SOCK_STREAM : TCP, SOCK_DGRAM : UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(sock, addr, port): 
    try:
        sock.connect( (addr, port) )  # tuple type
    except socket.error:
        print(f"Socket error : {socket.error}")
        return False
    except socket.timeout:
        print("Socket timeout")
        return False
    return True

def recv(sock, length):
    try:
        buf = sock.recv(length)  # blocking function
        if len(buf) == 0:
            print("Peer is disconnected")
            return None
    except socket.error:
        print(f"recv() : {socket.error}")
        return None
    return buf.decode("ascii")  # binary data to ascii string

# connect to www.naver.com
# default http port is 80
if connect(sock, "www.naver.com", 443):  # 443 : https port
    print("connected")
    # receive
    str = recv(sock, 100)
    if str is not None:
        print(f"Received {str}")
    sock.close()
