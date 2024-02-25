import threading
import signal
import sys

from src.Communication import Communication


def cleanup_and_exit():
    """
    Uzavře všechny otevřené sokety a ukončí program.
    """
    if Communication.udp_socket is not None:
        Communication.udp_socket.close()
    if Communication.tcp_server_socket is not None:
        Communication.tcp_server_socket.close()
    for client_socket in Communication.tcp_client_sockets:
        if client_socket is not None:
            client_socket.close()
    sys.exit(0)


def main():
    """
    Hlavní funkce aplikace. Nastavuje aplikaci a spouští vlákna pro UDP a TCP komunikaci.
    :return:
    """
    signal.signal(signal.SIGINT, lambda signal, frame: cleanup_and_exit())

    Communication.start_udp_listener()
    Communication.periodic_udp_discovery()

    tcp_server_thread = threading.Thread(target=Communication.start_tcp_server)
    tcp_server_thread.start()

    for peer_ip in Communication.discovered_peers:
        tcp_client_thread = threading.Thread(target=Communication.start_tcp_client, args=(peer_ip,))
        tcp_client_thread.start()

    send_thread = threading.Thread(target=Communication.send_messages)
    send_thread.start()

    receive_thread = threading.Thread(target=Communication.receive_messages)
    receive_thread.start()

    while True:
        pass


if __name__ == "__main__":
    main()
