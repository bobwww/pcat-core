from socket import socket, PF_PACKET, SOCK_RAW, ntohs


def sniff(conn):
    '''
    Sniff packets and send them to `conn`.
    conn may be any queue-like object with the method `send(x)`.
    Note: func never terminates
    '''
    with socket.socket(PF_PACKET, SOCK_RAW, ntohs(0x0003)) as sock:
        while True:
            recv = sock.recvfrom(65565)
            conn.send(recv)
