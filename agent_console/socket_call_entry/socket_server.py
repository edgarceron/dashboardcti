"""Manage a tcp server for the call on each agen as a new connection"""
import socket
import json
import time
import selectors
from datetime import datetime
import pytz
from _thread import start_new_thread
from agent_console.models import Audit, Agent, CurrentCallEntry, CedulaLlamada, ServerLog

class AgentConsoleSockectServer():
    server = None
    sel = selectors.DefaultSelector()

    @staticmethod
    def is_loged(id_agent):
        """ Checks if agent is loged to the call center module"""
        try:
            last_logon = Audit.objects.filter(
                id_agent=id_agent,
                id_break__isnull=True
            ).order_by('-datetime_init')[0]
            if last_logon.datetime_end == '' or last_logon.datetime_end is None:
                return True
            return False
        except:
            return False

    @staticmethod
    def agent_exist(id_agent):
        """Check if the agent still exist in the call_center db"""
        count = Agent.objects.filter(id=id_agent).count()
        if count == 1:
            return True
        return False

    @staticmethod
    def agent_current_call(id_agent):
        """Get the current call of the agent, None if there is no call"""
        try:
            query = CurrentCallEntry.objects.get(id_agent=id_agent)
            return query
        except CurrentCallEntry.DoesNotExist:
            return None

    @staticmethod
    def get_cedula(uniqueid):
        """Gets the document from the cedula_llamada table"""
        try:
            query = CedulaLlamada.objects.get(uniqueid=uniqueid)
            return query
        except CedulaLlamada.DoesNotExist:
            return None

    @staticmethod
    def get_answer(state, id_agent, current_call=None, log=False):
        """Returns the server answer given a state"""
        answer = {}
        if state == "1":
            answer['message'] = "El agente fue borrado del servidor de telefonía"
            answer['call'] = False
            answer['status'] = "No encontrado"

        elif state == "2":
            answer['message'] = "El agente no esta conectado, inicie sesión en su telefono"
            answer['call'] = False
            answer['status'] = "No conectado"

        elif state == "3":
            answer['message'] = "Esperando llamada"
            answer['call'] = False
            answer['status'] = "Conectado"

        elif state == "4":
            answer['message'] = "En llamada"
            answer['call'] = True
            answer['status'] = "Conectado"
            answer['phone'] = current_call.callerid
            answer['cedula'] = AgentConsoleSockectServer.get_cedula(current_call.uniqueid)

        if log:
            timezone = pytz.timezone("America/Bogota")
            server_log = ServerLog(
                event=state,
                agent=id_agent,
                description=answer['messsage'],
                datetime=timezone.localize(datetime.now())
            )
            server_log.save()
        answer = json.dumps(answer)
        return answer

    @staticmethod
    def threaded_client(connection, client_address):
        """Starts a new client as a thread"""
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(connection, events, data=None)

        try:
            print('connection from', client_address)
            # Receive the data in small chunks and retransmit it
            id_agent = ""

            while True:
                #Server recibe de cliente
                data = connection.recv(2048)
                data = data.decode("utf-8")
                print('received {!r}'.format(data))
                agent_info = json.loads(data)
                id_agent = agent_info['id']
                if id_agent != "":
                    break

            previus = -1
            state = ""
            past_call = ""
            while True:
                if not AgentConsoleSockectServer.agent_exist(id_agent):
                    state = "1"
                elif not AgentConsoleSockectServer.is_loged(id_agent):
                    state = "2"
                else:
                    current_call = AgentConsoleSockectServer.agent_current_call(id_agent)
                    if current_call is None:
                        state = "3"
                    else:
                        state = "4"
                if state == "4":
                    if current_call.uniqueid != past_call:
                        past_call = current_call.uniqueid
                        answer = AgentConsoleSockectServer.get_answer(state, id_agent, current_call)
                        connection.sendall(answer)
                elif previus != state:
                    previus = state
                    answer = AgentConsoleSockectServer.get_answer(state, id_agent)
                    connection.sendall(answer)

                time.sleep(1)
        finally:
            # Clean up the connection
            connection.close()

    @staticmethod
    def manage_incoming_data(recv_data):
        id_agent = ""
        if recv_data:
            recv_data = recv_data.decode("utf-8")
            print('received {!r}'.format(recv_data))
            agent_info = json.loads(recv_data)
            id_agent = agent_info['id']
        if recv_data == "close":
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
        return id_agent

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        id_agent = ""

        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            id_agent = self.manage_incoming_data(recv_data)

        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print("echoing", repr(data.outb), "to", data.addr)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
                
    # Create a TCP/IP socket
    def start_server(self):
        """ Starts the socket server """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', 16899)
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen()
        sock.setblocking(False)

        self.sel.register(sock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        accept_wrapper(key.fileobj)
                    else:
                        service_connection(key, mask)
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            sel.close()

#        while True:
#            print('waiting for a connection')
#            connection, client_address = self.server.accept()
#            connection.setblocking(False)
#            start_new_thread(self.threaded_client, (connection, client_address, ))

    def stop_server(self):
        """ Stops the socket server """
        self.server.close()
        print("Se detuvo el servidor exitosamente")
