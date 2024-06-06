import logging
import time
from threading import Thread
from opcua import Client

from utilities import AASArchive_utils
from utilities.Interactions_utils import delete_svc_request, get_next_svc_request
from utilities.OPC_UA_utils import sendDataOPCUA

# Some variables needed by this AAS Core
state = 'IDLE'
ready = False
WIP = False
machine_plan = []
processed_services = []

# OPC UA client
client = None

def main():

    # First, the status file is created
    AASArchive_utils.create_status_file()

    # Then, the initialization tasks are performed
    initialize_aas_core()

    AASArchive_utils.change_status('InitializationReady')

    # The AAS Core can start running
    run_aas_core()

def initialize_aas_core():
    """This method executes the required tasks to initialize the AAS Core. In this case, create the connection and
    execute a necessary ROS nodes."""

    print("Initializing the AAS Core...")

    # A ROS node corresponding to the AAS Core is executed.
    global client
    # Instanciar cliente
    client = Client("opc.tcp://192.168.1.71:4840")
    # Establecer conexión con servidor OPCUA
    client.connect()
    print("OPC UA client connected.")


def run_aas_core():

    print("AAS Core running...")
    AASArchive_utils.change_status('Running')

    # Each function will have its own thread of execution
    thread_func1 = Thread(target=handle_data_to_machine(), args=())
    thread_func2 = Thread(target=handle_data_from_machine(), args=())

    thread_func1.start()
    thread_func2.start()


def handle_data_to_machine():
    """This method handles the message and data to the transport. Thus, it obtains the interaction requests by the AAS
    Manager and send to necessary command to the asset."""

    while True:
        # TODO analizar los mensajes de peticiones del AAS Manager
        msgReceived = get_next_svc_request()
        global processed_services

        print(msgReceived)
        print("Processed svc: " + str(processed_services))

        if (msgReceived is not None) and (msgReceived['interactionID'] not in processed_services):

            global machine_plan
            machine_plan = [msgReceived['serviceData']['target']]
            print("InteractionID: " + str(msgReceived['interactionID']))

            # TODO, si ha llegado alguna peticion, enviar el comando a trabes del pub y pubCoord
            global WIP

            if len(machine_plan) > 0 and not WIP:

                # Coge la primera tarea de la lista
                task = machine_plan[0]

                # Identifica el tipo de tarea
                taskType = task.split(":")[0]
                # Obtiene la posición del almacén
                target = task.split(":")[1]

                # Si el servicio es "INTRODUCE"
                if taskType == "INTRODUCE":
                    # Se marca como 'ocupado'
                    WIP = True

                    print("         + Sending task: MACHINE AGENT >>> GATEWAY AGENT OPCUA")

                    print("     [!] Introducing package into shelf No.  " + str(target) + " [!]")
                    print("               + Sending data to OPC UA Server...")

                    result = sendDataOPCUA(taskType, target)

                    if result == "FINISHED":
                        print("+-----------------------------------------------------+")
                        print("| Package SUCCESSFULLY STORED in AUTOMATED WAREHOUSE  |")
                    else:
                        print("+-----------------** ERROR **-------------------+")
                        print("| Shelf No. "+ str(target)+" already OCCUPIED!! |")
                        print("+-----------------------------------------------+")
                # Si el servicio es "EXTRACT"
                else:
                    # Se marca como 'ocupado'
                    WIP = True

                    print("         + Sending task: MACHINE AGENT >>> GATEWAY AGENT OPCUA")

                    print("     [!] Extracting box from shelf No. " + str(target) + " [!]")
                    print("               + Sending data to OPC UA Server...")

                    result = sendDataOPCUA(taskType, target)

                    if result == "FINISHED":
                        print("+---------------------------------------------------------+")
                        print("| Package SUCCESSFULLY EXTRACTED from AUTOMATED WAREHOUSE |")
                        print("|   |____Establishing communication with [MACHINE AGENT]:machineagent@blah.im")

                        # TODO: para pruebas, eliminamos la peticion de servicio, como que ya se ha ofrecido
                        # delete_svc_request(msgReceived)
                        processed_services.append(msgReceived['interactionID'])
                    else:
                        print("\n+-----------------** ERROR **-------------------+")
                        print("|             Shelf No. " + str(target) + " is EMPTY!!            |")
                        print("+-----------------------------------------------+")
        else:
            print("No service requests yet.")
            time.sleep(2)







def handle_data_from_machine():
    """This method handles the message and data from the transport. Thus, it obtains the data from the asset with a ROS
    Subscriber node and send the necessary interaction command or response to the AAS Manager."""

    # Crea un nodo SUBSCRIBER, que se quedará a la escucha por el tópico /status
    # y notificará al agente del estado del transporte
    pass


if __name__ == '__main__':
    print('AAS Core to work with OPC UA')
    print('AAS Core starting...')
    # time.sleep(5)   # TODO para pruebas
    main()
    print('AAS ending...')

