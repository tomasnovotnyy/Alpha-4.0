import threading
import signal
import sys

from UDP import UDP

exit_flag = False


def cleanup_and_exit():
    if UDP.udp_socket is not None:
        UDP.udp_socket.close()
    if UDP.tcp_server_socket is not None:
        UDP.tcp_server_socket.close()
    for client_socket in UDP.tcp_client_sockets:
        if client_socket is not None:
            client_socket.close()
    sys.exit(0)


def signal_handler(signal, frame):
    global exit_flag
    exit_flag = True


def main():
    signal.signal(signal.SIGINT, signal_handler)

    UDP.start_udp_listener()
    UDP.periodic_udp_discovery()

    tcp_server_thread = threading.Thread(target=UDP.start_tcp_server)
    tcp_server_thread.start()

    for peer_ip in UDP.discovered_peers:
        tcp_client_thread = threading.Thread(target=UDP.start_tcp_client, args=(peer_ip,))
        tcp_client_thread.start()

    send_thread = threading.Thread(target=UDP.send_messages)
    send_thread.start()

    receive_thread = threading.Thread(target=UDP.receive_messages)
    receive_thread.start()

    global exit_flag
    while True:
        if exit_flag:
            cleanup_and_exit()
        pass


if __name__ == "__main__":
    main()
