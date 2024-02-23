import threading

from UDP import UDP


def main():
    UDP.start_udp_listener()
    UDP.periodic_udp_discovery()

    # Spustíme TCP server
    tcp_server_thread = threading.Thread(target=UDP.start_tcp_server, daemon=True)
    tcp_server_thread.start()

    # Spustíme TCP klienta pro každého nalezeného peeru
    for peer_ip in UDP.discovered_peers:
        tcp_client_thread = threading.Thread(target=UDP.start_tcp_client, args=(peer_ip,), daemon=True)
        tcp_client_thread.start()

    send_thread = threading.Thread(target=UDP.send_messages, daemon=True)
    send_thread.start()

    receive_thread = threading.Thread(target=UDP.receive_messages, daemon=True)
    receive_thread.start()

    try:
        input()  # Program bude běžet, dokud uživatel nezadá Enter
    finally:
        UDP.udp_socket.close()
        UDP.tcp_server_socket.close()
        for client_socket in UDP.tcp_client_sockets:
            client_socket.close()


if __name__ == "__main__":
    main()
