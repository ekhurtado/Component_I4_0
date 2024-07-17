from urllib.parse import parse_qs

import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

# XMPP_SERVER = 'worker4'
XMPP_SERVER = 'ejabberd'


class GUIAgent(Agent):
    class SendBehaviour(OneShotBehaviour):
        async def run(self):
            # Prepare the ACL message
            data_json = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(self.msg_data).items()}
            print(data_json)

            # Create the Message object
            print("Building the message to send to the agent with JID: " + str(data_json['receiver']))
            receiver = data_json['receiver'] + '@' + data_json['server']
            msg = Message(to=receiver, thread=data_json['thread'])
            msg.set_metadata('performative', data_json['performative'])
            msg.set_metadata('ontology', data_json['ontology'])

            if data_json['messageType'] == 'normal':  # message body with normal format
                msg.body = data_json['normalMessage']
            elif len(data_json['messageType']) == 2:
                msg.body = '{"serviceID": "' + data_json['serviceID'] + \
                       '", "serviceType": "' + data_json['serviceType'] + \
                       '", "serviceData": ' + data_json['serviceData'] + '}'
            print(msg)

            print("Sending the message...")
            await self.send(msg)
            print("Message sent!")

    class NegBehaviour(OneShotBehaviour):
        async def run(self):
            # Prepare the ACL message
            data_json = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(self.msg_data).items()}
            print(data_json)

            # Create the Message object
            # TODO mirar como se envian las negociaciones
            receivers_jid = None
            if ',' in data_json['receiver']:
                receivers_jid = data_json['receiver'].split(',')
            else:
                receivers_jid = [data_json['receiver']]

            print(receivers_jid)

            for jid in receivers_jid:
                print("Building the negotiation message to send to the agent with JID: " + jid)
                receiver = jid + '@' + data_json['server']
                msg = Message(to=receiver, thread=data_json['thread'])
                msg.set_metadata('performative', data_json['performative'])
                msg.set_metadata('ontology', data_json['ontology'])
                msg.set_metadata('neg_requester_jid', str(self.agent.jid))
                msg.set_metadata('targets', str(receivers_jid))
                msg.body = data_json['criteria']

                print(msg)

                print("Sending the message...")
                await self.send(msg)
                print("Message sent!")

            print("All negotiation messages sent!")

    async def setup(self):
        print("Hello World! I'm sender agent {}".format(str(self.jid)))
        print("GUIAgent started")
        self.acl_sent = False  # se inicializa en False
        self.neg_sent = False  # se inicializa en False

    async def acl_post_controller(self, request):

        self.acl_sent = False  # se inicializa en False
        print("HA LLEGADO AL POST DEL AGENTE: " + str(self.jid))
        print(request)
        data_bytes = b''
        async for line in request.content:
            data_bytes = data_bytes + line
        data_str = data_bytes.decode('utf-8')
        print(data_str)

        self.b = self.SendBehaviour()
        self.b.msg_data = data_str
        self.add_behaviour(self.b)
        print("Behaviour added to the agent")
        await self.b.join()
        self.acl_sent = True

        return {"status": "OK"}

    async def neg_post_controller(self, request):

        self.neg_sent = False  # se inicializa en False
        print("HA LLEGADO AL POST DEL AGENTE: " + str(self.jid))
        print(request)
        data_bytes = b''
        async for line in request.content:
            data_bytes = data_bytes + line
        data_str = data_bytes.decode('utf-8')
        print(data_str)

        self.b = self.NegBehaviour()
        self.b.msg_data = data_str
        self.add_behaviour(self.b)
        print("Behaviour added to the agent")
        await self.b.join()
        self.neg_sent = True

        return {"status": "OK"}


async def hello_controller(request):
    print(request)
    return {"status": "OK"}


async def main():
    aas_id = 'guiagent'  # For testing
    # Build the agent jid and password
    agent_jid = aas_id + '@' + XMPP_SERVER
    passwd = '123'

    # DATOS PARA PRUEBAS CON ANONYM.IM
    # agent_jid = "gui_agent@anonym.im"
    # passwd = "gcis1234"

    gui_agent = GUIAgent(agent_jid, passwd)
    gui_agent.agent_name = 'gui_agent'

    # Add customized webpages
    gui_agent.web.add_get("/acl_message", hello_controller, "/htmls/send_acl.html")
    gui_agent.web.add_post("/acl_message/submit", gui_agent.acl_post_controller, "/htmls/send_acl_submit.html")

    gui_agent.web.add_get("/negotiation", hello_controller, "/htmls/negotiation.html")
    gui_agent.web.add_post("/negotiation/submit", gui_agent.neg_post_controller, "/htmls/negotiation_submit.html")

    gui_agent.web.add_get("/editor", hello_controller, "/htmls/own_programming_language_editor.html")
    gui_agent.web.add_post("/editor/submit", gui_agent.acl_post_controller, "/htmls/own_programming_language_editor.html")

    gui_agent.web.add_get("/aas_library", hello_controller, "/htmls/aas_library.html")
    print("All HTMLs added.")

    # Since the agent object has already been created, the agent will start
    await gui_agent.start()
    gui_agent.web.start(hostname="0.0.0.0", port="10000")  # https://spade-mas.readthedocs.io/en/latest/web.html#
    gui_agent.web.add_menu_entry("Send ACL message", "/acl_message",
                                    "fa fa-envelope")  # https://github.com/javipalanca/spade/blob/master/docs/web.rst#menu-entries
    gui_agent.web.add_menu_entry("Negotiation", "/negotiation", "fa fa-comments")
    gui_agent.web.add_menu_entry("Programming language editor", "/editor", "fa fa-code")
    gui_agent.web.add_menu_entry("AAS Library", "/aas_library", "fa fa-book")
    # The main thread will be waiting until the agent has finished
    await spade.wait_until_finished(gui_agent)


if __name__ == '__main__':
    print("Initializing GUI SPADE agent program...")

    # Run main program with SPADE
    spade.run(main())
