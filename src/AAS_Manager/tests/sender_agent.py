import codecs
import json
import os
import time

import spade
from aioxmpp import stream
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

# XMPP_SERVER = 'worker4'
XMPP_SERVER = 'ejabberd'

class SenderAgent(Agent):
    class SendBehaviour(OneShotBehaviour):
        async def run(self):
            # Prepare the ACL message
            performative = os.environ.get('PERFORMATIVE')
            ontology = os.environ.get('ONTOLOGY')
            body = os.environ.get('MSG_BODY')
            receiver = os.environ.get('RECEIVER_JID')

            print("Building the message to send to the agent with JID: " + str(receiver))

            msg = Message(to=receiver)
            if performative is not None:
                msg.set_metadata('performative', performative)
                print("The message has the performative: " + str(performative))
            if ontology is not None:
                msg.set_metadata('ontology', ontology)
                print("The message has the ontology: " + str(ontology))
            print("The message content is: " + str(body))
            msg.body = body

            time.sleep(10)  # espera de 10s para que de tiempo a leer la consola
            print("Sending the message...")
            await self.send(msg)

            # set exit_code for the behaviour
            self.exit_code = "Job Finished!"

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("Hello World! I'm sender agent {}".format(str(self.jid)))
        print("SenderAgent started")
        self.b = self.SendBehaviour()
        # self.add_behaviour(self.b)

    async def post_controller(self, request):
        print("HA LLEGADO AL POST DEL AGENTE: " + str(self.jid))
        print(request)
        data_bytes = b''
        async for line in request.content:
            print(line)
            data_bytes = data_bytes + line
        data_str = data_bytes.decode('utf-8')
        print(data_str)
        return {"number": 42}

async def hello_controller(request):
    print(request)
    return {"number": 42}




async def main():

    aas_id = 'senderagent'  # For testing
    # Build the agent jid and password
    agent_jid = aas_id + '@' + XMPP_SERVER
    passwd = '123'

    agent_jid = "gcis3@anonym.im"
    passwd = "gcis1234"
    sender_agent = SenderAgent(agent_jid, passwd)

    # Add customized webpage
    # sender_agent.web.add_get("/hello", hello_controller, "/hello.html")
    sender_agent.web.add_get("/acl_message", hello_controller, "/send_acl.html")
    sender_agent.web.add_post("/acl_message/submit", sender_agent.post_controller, "/send_acl.html")
    sender_agent.web.add_get("/editor", hello_controller, "/own_programming_language_editor.html")
    sender_agent.web.add_post("/editor/submit", sender_agent.post_controller, "/own_programming_language_editor.html")
    sender_agent.web.add_get("/aas_library", hello_controller, "/aas_library.html")
    print("Hello HTML added")

    # Since the agent object has already been created, the agent will start
    await sender_agent.start()
    sender_agent.web.start(hostname="0.0.0.0", port="10000")    # https://spade-mas.readthedocs.io/en/latest/web.html#
    sender_agent.web.add_menu_entry("Send ACL message", "/acl_message", "fa fa-envelope")  # https://github.com/javipalanca/spade/blob/master/docs/web.rst#menu-entries
    sender_agent.web.add_menu_entry("Programming language editor", "/editor", "fa fa-envelope")
    sender_agent.web.add_menu_entry("AAS Library", "/aas_library", "fa fa-envelope")
    # The main thread will be waiting until the agent has finished
    await spade.wait_until_finished(sender_agent)

if __name__ == '__main__':
    print("Initializing AAS Manager program...")

    # Run main program with SPADE
    spade.run(main())
