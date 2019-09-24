'''
Defines the most commonly used functionality of pwntools
'''

import socket
import struct
import time

class remote:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def recvuntil(self, until):
        data = ''
        while until not in data:
            d = self.sock.recv(1)
            if not d: break
            data += d
        return data

    def recvline(self, keepend=False):
        data = self.recvuntil('\n')
        if not keepend:
            return data[:-1]
        return data

    def recv(self, n):
        return self.sock.recv(n)

    def recvall(self, timeout=2):
        self.sock.setblocking(0)

        total_data = []
        data = ''
        begin = time.time()

        while 1:
            #if you got some data, then break after wait sec
            if total_data and time.time() - begin > timeout:
                break
            #if you got no data at all, wait a little longer
            elif time.time() - begin > timeout * 2:
                break
            try:
                data = self.sock.recv(8192)
                if data:
                    total_data.append(data)
                    begin=time.time()
                else:
                    time.sleep(0.1)
            except:
                pass

        self.sock.setblocking(1)
        return ''.join(total_data)

    def sendline(self, line):
        self.sock.sendall(line + '\n')

    def sendlineafter(self, after, line):
        self.recvuntil(after)
        self.sock.sendall(line + '\n')

    def send(self, data):
        self.sock.sendall(data)

    def close(self):
        self.sock.close()

    def interactive(self):
        try:
            while True:
                self.sock.sendall(raw_input('$ ') + '\n')
                resp = self.recvall(0.2)
                if resp:
                    print resp,

        except KeyboardInterrupt:
            return

    def clean(self):
        self.recvall()


def p32(data):
    return struct.pack('<I', data)

def u32(data):
    return struct.unpack('<I', data)[0]

def p64(data):
    return struct.pack('<Q', data)

def u64(data):
    return struct.unpack('<Q', data)[0]

