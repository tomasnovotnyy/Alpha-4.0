import socket
import threading
import time
import json


class UDP:
    udp_socket = None
    my_peer_id = "Tomáš"  # Změňte podle potřeby

    @staticmethod
    def start_udp_listener():
        try:
            UDP.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDP.udp_socket.bind(('', 9876))
            udp_listener_thread = threading.Thread(target=UDP.udp_listener)
            udp_listener_thread.start()
        except Exception as ex:
            print(ex)

    @staticmethod
    def udp_listener():
        while True:
            data, addr = UDP.udp_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print("Received UDP: " + message)

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
        # Zde můžete implementovat logiku pro odesílání TCP zpráv ostatním peerům
        pass

    @staticmethod
    def receive_messages():
        # Zde můžete implementovat logiku pro příjem TCP zpráv od ostatních peerů
        pass
