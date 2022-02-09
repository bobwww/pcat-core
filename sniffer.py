from socket import socket, PF_PACKET, SOCK_RAW, ntohs


def sniff(conn):
    with socket.socket(PF_PACKET, SOCK_RAW, ntohs(0x0003)) as sock:
        while True:
            recv = sock.recvfrom(65565)
            conn.send(recv)
