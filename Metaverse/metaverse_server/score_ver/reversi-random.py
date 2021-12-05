import threading
import socket
import time
import math
import random

isRunning = True
reversiPos = None       # 리버시 위치
turnColor = None
curTurn = "none"
hints = []
name = None

def work1(sock):
    global isRunning, reversiPos, turnColor, curTurn, hints, name
    while isRunning:
        try:
            data = sock.recv(4)
            plen = int(data)
            data = sock.recv(plen)
        except socket.error:
            print("E2")
            isRunning = False
            return
        sdata = data.decode()
        ss = sdata.split()
        if ss[0] == "update":
            thints = []
            for r in range(8):
                print("+---"*8+"+")
                for c in range(8):
                    if ss[2][r*8+c] == '0':
                        print(f"|{r*8+c:^3}", end="")
                        thints.append(r*8+c)
                    elif ss[2][r*8+c] == '3':
                        print("|   ", end="")
                    elif ss[2][r*8+c] == '1':
                        print("| O ", end="")
                    elif ss[2][r*8+c] == '2':
                        print("| X ", end="")
                print("|")
            print("+---"*8+"+")
            curTurn = ss[3]
            hints = thints
        elif ss[0] == "worlddata":
            if ss[1] == "Reversi":
                reversiPos = (float(ss[2]), float(ss[3]))
        elif ss[0] == "action":
            print(sdata)
            if ss[1] == name and ss[2] == "Reversi" and ss[3] == "join":
                turnColor = ss[4]
                print("나의 돌 색깔은 %s."%turnColor)
        else:
            print(sdata)

def work2(sock):
    global isRunning, reversiPos, turnColor, curTurn, hints, name
    # {name}란 이름으로 join
    name = f"reversi_{random.randrange(1, 10000):04}"
    send(sock, f"join {name}")
    send(sock, f"avatar {name} 0")
    send(sock, f"look {name} 0 0 0 0 0")
    # 리버시 게임판으로 자동 이동하기 위해서 reversiPos 기다림
    while reversiPos == None:
        time.sleep(5.0)
    # reversi 판 있는 곳의 각도 구하기
    rangle = math.degrees(math.atan2(reversiPos[1], reversiPos[0]))
    send(sock, f"move {name} 0 0 {rangle} 1 0")
    rdistance = math.sqrt(reversiPos[0]**2 + reversiPos[1]**2)-1.5
    time.sleep(rdistance)
    finalPosX = rdistance*math.cos(math.radians(rangle))
    finalPosY = rdistance*math.sin(math.radians(rangle))
    send(sock, f"move {name} {finalPosX} {finalPosY} {rangle} 0 0")
    while True:
        # reversi join
        send(sock, f"action {name} Reversi join")
        # 게임이 시작할때까지 기다림
        while curTurn == "none":
            time.sleep(2.5)
        # 게임이 끝날때까지 계속
        while curTurn != "none":
            # 현재의 턴이 내 턴인 경우
            if curTurn == turnColor and len(hints) > 0:
                p = random.choice(hints)
                send(sock, f"action {name} Reversi place {p}")
            time.sleep(1.0)
        print("Quit play")
        time.sleep(2.0)
    
    """
    while isRunning:
        s = input(">> ")
        if s == "/quit":
            isRunning = False
            return
        data = s.encode()
        packet = ("%04d"%len(data)).encode()+data
        sock.send(packet)
    """

# sock으로 mesg를 보내는 함수
def send(sock, mesg):
    # packet 인코딩
    packet = ("%04d%s"%(len(mesg), mesg)).encode()
    sock.send(packet)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect( ("127.0.0.1", 8888) )
except socket.error:
    print(f"Network error {socket.error}")
    quit()
    
print("Connection is established")
thread1 = threading.Thread(target=work1, args=(sock,))
thread1.start()
thread2 = threading.Thread(target=work2, args=(sock,))
thread2.start()
thread1.join()
thread2.join()
