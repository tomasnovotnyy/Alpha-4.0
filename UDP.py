import socket
import threading
import time
import json


class UDP:

    udp_socket = None
    my_peer_id = "Tomas Novotny, C4b"
    tcp_server_socket = None
    tcp_client_sockets = []
    messages = {}
    discovered_peers = set()

    @staticmethod
    def udp_listener():
        while True:
            data, addr = UDP.udp_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print("Received UDP: " + message)
            UDP.discovered_peers.add(addr[0])  # Přidáme IP adresu do setu discovered_peers

    @staticmethod
    def start_udp_listener():
        try:
            UDP.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDP.udp_socket.bind(('', 9876))
            UDP.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Přidáno nastavení pro povolení
            # broadcast zpráv
            udp_listener_thread = threading.Thread(target=UDP.udp_listener)
            udp_listener_thread.start()
        except Exception as ex:
            print(ex)

    @staticmethod
    def periodic_udp_discovery():
        while True:
            UDP.send_udp_discovery()
            time.sleep(5)

    @staticmethod
    def send_udp_discovery():
        udp_message = json.dumps({"command": "hello", "peer_id": UDP.my_peer_id})
        UDP.udp_socket.sendto(udp_message.encode('utf-8'), ('<broadcast>', 9876))


    @staticmethod
    def send_messages():
        while True:
            message = input("Enter a message: ")
            UDP.send_tcp_message(message)

    @staticmethod
    def receive_messages():
        while True:
            for message_id, message in UDP.messages.items():
                print(f"{message['peer_id']}: {message['message']}")
                time.sleep(1)

    @staticmethod
    def start_tcp_server():
        UDP.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        UDP.tcp_server_socket.bind(('', 9876))
        UDP.tcp_server_socket.listen()
        while True:
            client_socket, addr = UDP.tcp_server_socket.accept()
            client_thread = threading.Thread(target=UDP.handle_client, args=(client_socket,))
            client_thread.start()

    @staticmethod
    def handle_client(client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = json.loads(data.decode('utf-8'))
            if message['command'] == 'hello':
                response = json.dumps({"status": "ok", "messages": UDP.messages})
                client_socket.send(response.encode('utf-8'))
            elif message['command'] == 'new_message':
                UDP.messages[message['message_id']] = {"peer_id": message['peer_id'], "message": message['message']}
                response = json.dumps({"status": "ok"})
                client_socket.send(response.encode('utf-8'))

    @staticmethod
    def start_tcp_client(peer_ip):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peer_ip, 9876))
        UDP.tcp_client_sockets.append(client_socket)
        hello_message = json.dumps({"command": "hello", "peer_id": UDP.my_peer_id})
        client_socket.send(hello_message.encode('utf-8'))
        data = client_socket.recv(1024)
        response = json.loads(data.decode('utf-8'))
        if response['status'] == 'ok':
            UDP.merge_messages(response['messages'])

    @staticmethod
    def send_tcp_message(message):
        message_id = str(int(time.time() * 1000))
        for client_socket in UDP.tcp_client_sockets:
            new_message = json.dumps({"command": "new_message", "message_id": message_id, "message": message})
            client_socket.send(new_message.encode('utf-8'))

    @staticmethod
    def merge_messages(new_messages):
        for message_id, message in new_messages.items():
            if message_id not in UDP.messages:
                UDP.messages[message_id] = message