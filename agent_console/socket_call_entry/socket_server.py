"""Manage a tcp server for the call on each agen as a new connection"""
import socket
import json
import time
from _thread import start_new_thread
from agent_console.models import Audit, Agent, CurrentCallEntry, CedulaLlamada

def is_loged(id_agent):
    """ Checks if agent is loged to the call center module"""
    try:
        last_logon = Audit.objects.filter(
            id_agent=id_agent, 
            id_break__isnull=False
        ).order_by('-datetime_init')[0]
        print(last_logon)
        if last_logon.datetime_end == '':
            return True
        return False
    except:
        return False

def agent_exist(id_agent):
    """Check if the agent still exist in the call_center db"""
    count = Agent.objects.filer(id=id_agent).count()
    if count == 1:
        return True
    return False

def agent_current_call(id_agent):
    """Get the current call of the agent, None if there is no call"""
    try:
        query = CurrentCallEntry.objects.get(id_agent=id_agent)
        return query
    except CurrentCallEntry.DoesNotExist:
        return None

def get_cedula(uniqueid):
    """Gets the document from the cedula_llamada table"""
    try:
        query = CedulaLlamada.objects.get(uniqueid=uniqueid)
        return query
    except CedulaLlamada.DoesNotExist:
        return None

def get_answer(state, current_call=None):
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
        answer['cedula'] = get_cedula(current_call.uniqueid)

    answer = json.dumps(answer)
    return answer

def threaded_client(connection, client_address):
    """Starts a new client as a thread"""
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        id_agent = ""

        while True:
            #Server recibe de cliente
            data = connection.recv(2048)
            print('received {!r}'.format(data))
            agent_info = json.loads(data)
            id_agent = agent_info['id']
            if id_agent != "":
                break

        previus = -1
        state = ""
        past_call = ""
        while True:
            if not agent_exist(id_agent):
                state = "1"
            elif not is_loged(is_loged):
                state = "2"
            else:
                current_call = agent_current_call(id_agent)
                if current_call is None:
                    state = "3"
                else:
                    state = "4"
            if state == "4":
                if current_call.uniqueid != past_call:
                    past_call = current_call.uniqueid
                    answer = get_answer(state, current_call)
                    connection.sendall(answer)
            elif previus != state:
                previus = state
                answer = get_answer(state)
                connection.sendall(answer)
            
            time.sleep(1)
    finally:
        # Clean up the connection
        connection.close()

# Create a TCP/IP socket
def startServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 16899)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        start_new_thread(threaded_client, (connection, client_address, ))
