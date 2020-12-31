import struct
import time
from socket import *
# import thread module
from _thread import *
import threading

print_lock = threading.Lock()
teams = []
group1 = []
group2 = []
score1 = 0
score2 = 0
clients = []
check = []
BROADCAST = 60
PLAYTIME = 10
Finished = False
Start = True
SERVER_IP = gethostbyname(gethostname())
TCPORT = 30546
UDPORT = 13117


def broadcast():
    global BROADCAST, Finished
    # initializing socket
    server_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # Using broadcast
    server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    # binding port and host
    server_socket.bind((SERVER_IP, TCPORT))
    # Setting timeout for establish connection
    server_socket.settimeout(0.2)
    # The massage that will be broadcast
    msg = struct.pack('Ibh', 0xfeedbeef, 0x2, TCPORT)

    # Setting time for the server to broadcast the message every 1 second
    t_end = time.time() + BROADCAST
    print("server listening . . .")
    while time.time() < t_end:
        server_socket.sendto(msg, ('<broadcast>', UDPORT))
        time.sleep(1)
    while not Finished:
        time.sleep(1)


def mission(client):
    global PLAYTIME, Finished
    # Server receives Team Name from client
    data = client.recv(1024)
    data = data.decode('ascii')
    print(data)

    # Server assign team to a group
    teams.append(data)
    j = int
    if len(group1) < 2:
        group1.append(data)
        j = 1
    else:
        group2.append(data)
        j = 2

    print_lock.release()

    while len(group2) != 2:
        time.sleep(1)

    global score1
    global score2
    score1 = 0
    score2 = 0

    if len(group1) == 2 and len(group2) == 2:
        # Server sends start message
        msg = "\nWelcome to Keyboard Spamming Battle Royal!\n " \
              "Group 1: \n" \
              "== \n" + str(group1[0]) + str(group1[1]) + "\n\n" + "Group 2: \n" + "== \n" + str(group2[0]) + str(group2[1]) + "\n" + \
              "Start pressing keys (press enter after each key)"
        client.send(msg.encode('ascii'))

        time.sleep(1)

        count = 0
        t_end = time.time() + PLAYTIME
        data = None
        # Server receives messages for a limited time (Play time)
        while time.time() < t_end:
            if data:
                print(data.decode('ascii'))
                count += 1
            data = client.recv(1)

        # Server calculates each team score
        print_lock.acquire()
        if j == 1:
            score1 += count
        else:
            score2 += count
        check.append(1)
        print_lock.release()

        while len(check) != 4:
            time.sleep(1)

        time.sleep(1)

        # Server sends each team their own score and the winning team declaration
        msg = "you typed: " + str(count) + " keys \n"
        client.send(msg.encode('ascii'))
        if score1 > score2:
            msg = "Group 1 typed in " + str(score1) + " characters. Group 2 typed in " + str(score2) + " characters. \n" \
                                                                                                           "Group 1 wins!"
        else:
            msg = "Group 1 typed in " + str(score1) + " characters. Group 2 typed in " + str(score2) + " characters. \n" \
                                                                                                           "Group 2 wins!"
        client.send(msg.encode('ascii'))

        time.sleep(1.5)
        Finished = True

    client.close()


def establish_tcp():
    global Finished, Start
    count = 0
    # initializing socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.settimeout(1)

    # binding port and host
    server_socket.bind((SERVER_IP, TCPORT))
    print("server listening TCP . . .")
    # waiting for a client to connect
    server_socket.listen(4)
    while not Finished:
        try:
            # accept connection
            client, addr = server_socket.accept()
        except:
            continue
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        count += 1
        clients.append(client)
        # each client get a thread running his own version of 'mission'
        start_new_thread(mission, (client,))

    print("Game over, sending out offer requests...")
    server_socket.close()
    Start = True


while True:
    if Start:
        Start = False
        Finished = False
        check.clear()
        clients.clear()
        score1 = 0
        score2 = 0
        group1.clear()
        group2.clear()
        teams.clear()

        t1 = threading.Thread(target=broadcast)
        t2 = threading.Thread(target=establish_tcp)

        t1.start()
        t2.start()

        t1.join()
        t2.join()
