#!/usr/bin/env python3

import socket
import selectors
import types
import json

class AgentConsoleSocketClient():
    sel = selectors.DefaultSelector()

    def start_connection(self, host, port, data):
        server_addr = (host, port)
        print("starting connection to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(sock, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                print("received", repr(recv_data), "from connection", data.connid)

            if recv_data == "close":
                print("closing connection", data.connid)
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.message:
                print("sending", repr(data.message), "to connection")
                sent = sock.send(data.outb)  # Should be ready to write
                data.message = 0


    def start_client(self):
        host = '127.0.0.1'
        port = 16899
        json_data = json.dumps({'id':'103'})
        data = types.SimpleNamespace(
                    message=json_data
        )
        self.start_connection(host, int(port), data)

        try:
            while True:
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        self.service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()
