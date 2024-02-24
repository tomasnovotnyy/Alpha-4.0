import socket
import threading
import time
import json


class Communication:
    """
    Třída `Communication` je statická třída, která zvládá komunikaci pomocí socketů jak pro Communication, tak pro TCP.
    Je navržena tak, aby objevovala vrstevníky, odesílala a přijímala zprávy pomocí protokolů Communication a TCP.
    """

    udp_socket = None
    my_peer_id = "Tomas Novotny, C4b"
    tcp_server_socket = None
    tcp_client_sockets = []
    messages = {}
    discovered_peers = set()

    @staticmethod
    def udp_listener():
        """
        Naslouchá příchozím paketům Communication a přidává IP adresu odesílatele do sady `discovered_peers`.
        """
        while True:
            data, addr = Communication.udp_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print("Received Communication: " + message)
            Communication.discovered_peers.add(addr[0])  # Přidáme IP adresu do setu discovered_peers

    @staticmethod
    def start_udp_listener():
        """
        Inicializuje socket Communication a spustí naslouchání Communication v novém vlákně.
        """
        try:
            Communication.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            Communication.udp_socket.bind(('', 9876))
            Communication.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # broadcast zpráv
            udp_listener_thread = threading.Thread(target=Communication.udp_listener)
            udp_listener_thread.start()
        except Exception as ex:
            print(ex)

    @staticmethod
    def periodic_udp_discovery():
        """
        Pravidelně odesílá zprávy o objevení Communication na broadcastovou adresu.
        """
        while True:
            Communication.send_udp_discovery()
            time.sleep(5)

    @staticmethod
    def send_udp_discovery():
        """
        Odesílá zprávu o objevení Communication na broadcastovou adresu.
        """
        udp_message = json.dumps({"command": "hello", "peer_id": Communication.my_peer_id})
        Communication.udp_socket.sendto(udp_message.encode('utf-8'), ('<broadcast>', 9876))

    @staticmethod
    def send_messages():
        """
        Neustále vyzývá uživatele k zadání zprávy a odesílá ji všem připojeným klientům TCP.
        """
        while True:
            message = input("Enter a message: ")
            Communication.send_tcp_message(message)

    @staticmethod
    def receive_messages():
        """
        Neustále vypisuje přijaté zprávy do konzole.
        """
        while True:
            for message_id, message in Communication.messages.items():
                print(f"{message['peer_id']}: {message['message']}")
                time.sleep(1)

    @staticmethod
    def start_tcp_server():
        """
        Inicializuje serverový socket TCP a naslouchá příchozím spojením v novém vlákně.
        """
        Communication.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Communication.tcp_server_socket.bind(('', 9876))
        Communication.tcp_server_socket.listen()
        while True:
            client_socket, addr = Communication.tcp_server_socket.accept()
            client_thread = threading.Thread(target=Communication.handle_client, args=(client_socket,))
            client_thread.start()

    @staticmethod
    def handle_client(client_socket):
        """
        Řeší komunikaci s připojeným klientem TCP.
        """
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = json.loads(data.decode('utf-8'))
            if message['command'] == 'hello':
                response = json.dumps({"status": "ok", "messages": Communication.messages})
                client_socket.send(response.encode('utf-8'))
            elif message['command'] == 'new_message':
                Communication.messages[message['message_id']] = {"peer_id": message['peer_id'], "message": message['message']}
                response = json.dumps({"status": "ok"})
                client_socket.send(response.encode('utf-8'))

    @staticmethod
    def start_tcp_client(peer_ip):
        """
        Připojuje se k serveru TCP na dané IP adrese a začíná vyměňovat zprávy.
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peer_ip, 9876))
        Communication.tcp_client_sockets.append(client_socket)
        hello_message = json.dumps({"command": "hello", "peer_id": Communication.my_peer_id})
        client_socket.send(hello_message.encode('utf-8'))
        data = client_socket.recv(1024)
        response = json.loads(data.decode('utf-8'))
        if response['status'] == 'ok':
            Communication.merge_messages(response['messages'])

    @staticmethod
    def send_tcp_message(message):
        """
        Odesílá zprávu všem připojeným klientům TCP.
        """
        message_id = str(int(time.time() * 1000))
        for client_socket in Communication.tcp_client_sockets:
            new_message = json.dumps({"command": "new_message", "message_id": message_id, "message": message})
            client_socket.send(new_message.encode('utf-8'))

    @staticmethod
    def merge_messages(new_messages):
        """
        Sloučí nově přijaté zprávy do slovníku `messages`.
        """
        for message_id, message in new_messages.items():
            if message_id not in Communication.messages:
                Communication.messages[message_id] = message
