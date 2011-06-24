import threading
import time
import socket

def make_connection(host, port, data_to_send):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(data_to_send)
    s.send('\r\n')
    b = []
    while True:
        data = s.recv(1024)
        if data:
            b.append(data)
        else:
            break

    return ''.join(b)


def t_connection(host, port, d):
    start = time.time()
    make_connection(host, port, d)
    print d, 'took', time.time() - start

if __name__ == '__main__':

    import sys
    host, port = sys.argv[1].split(':')
    data_to_send = sys.argv[2:]

    threads = []
    overallstart = time.time()
    for d in data_to_send:
        t = threading.Thread(target=t_connection, args=(host, int(port), d))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print 'FINISHED in', time.time() - overallstart

