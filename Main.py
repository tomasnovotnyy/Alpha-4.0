import threading

from UDP import UDP


def main():
    UDP.start_udp_listener()
    UDP.periodic_udp_discovery()

    send_thread = threading.Thread(target=UDP.send_messages)
    send_thread.start()

    receive_thread = threading.Thread(target=UDP.receive_messages)
    receive_thread.start()

    try:
        input()  # Program bude běžet, dokud uživatel nezadá Enter
    finally:
        UDP.udp_socket.close()


if __name__ == "__main__":
    main()
