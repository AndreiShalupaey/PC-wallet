import socket
import hashlib
import uuid
import datetime

option = ""
addres = ""
hash_pass = ""
salt = ""
option2 = ""

host = "localhost"
port = "9090"

print("Connect to node: ")
while True:
    print("1. Generate new wallet")
    print("2. Load wallet")
    print("3. Configure")
    print("4. Exit")
    option = input()
    if (option == "1"):
        password = input("Enter password to wallet: ")
        salt = uuid.uuid4().hex
        date_time = datetime.datetime.now()
        addres = hashlib.sha256(salt.encode() + password.encode() + str(date_time).encode()).hexdigest()
        hash_pass = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
        password = ""
        wallet_config_file = open("wallet_config", "w")
        wallet_config_file.write(addres)
        wallet_config_file.write(str(hash_pass))
        wallet_config_file.close()
        addres = ""
        hash_pass = ""
        salt = ""
        count_coins = 0
    if (option == "2"):
        config_host_file = open("host_config", "r")
        host = config_host_file.read()
        config_host_file.close()
        port_config_file = open("port_config", "r")
        port = port_config_file.read()
        port_config_file.close()
        sock = socket.socket()
        sock.connect((host, int(port)))
        addres = ""
        hash_pass = ""
        salt = ""
        wallet_config_file = open("wallet_config", "r")
        wallet_config_read_file = str(wallet_config_file.read())
        wallet_config_file.close()
        for i in range(0,64):
            addres = addres + wallet_config_read_file[i]
        for i in range(64,128):
            hash_pass = hash_pass + wallet_config_read_file[i]
        for i in range(129,161):
            salt = salt + wallet_config_read_file[i]
        password = input("Enter password: ")
        if (hash_pass != hashlib.sha256(salt.encode() + password.encode()).hexdigest()):
            print("Wrong password!!!")
            break
        hash_pass = ""
        salt = ""
        print("Welcome to wallet")
        sock.send('sync '.encode() + addres.encode())
        count_coins = int(sock.recv(1024).decode())
        print("Addres: ", addres)
        print("Coins: ", count_coins)
        while True:
            print("1. Send coins")
            print("2. Update wallet")
            print("3. Exit")
            option2 = input()
            if (option2 == "1"):
                addres_to = input("Input addres recipient: ")
                cost_to = input("Input count coins: ")
                if ((int(cost_to) <= int(count_coins)) and (int(cost_to) >= 0)):
                    sock.send("send ".encode() + addres.encode() + addres_to.encode() + cost_to.encode())
            if (option2 == "2"):
                sock.send("sync ".encode() + addres.encode())
                count_coins = int(sock.recv(1024).decode())
                print("Coins: ", count_coins)
            if (option2 == "3"):
                break
    if (option == "3"):
        host = input("input addres of node: ")
        config_host_file = open("host_config", "w")
        config_host_file.write(str(host))
        config_host_file.close()
        host = ""
        port_config_file = open("port_config", "w")
        port = input("Input node port: ")
        port_config_file.write(str(port))
        port_config_file.close()
    if (option == "4"):
        break

sock.close()