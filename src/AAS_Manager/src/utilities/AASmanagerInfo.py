from spade.template import Template


class AASmanagerInfo:
    """This class contains the general information about the AAS Manager."""

    # Variables related to states of the FSM
    BOOTING_STATE_NAME = 'BOOTING'
    RUNNING_STATE_NAME = 'RUNNING'
    STOPPING_STATE_NAME = 'STOPPING'
    IDLE_STATE_NAME = 'IDLE'

    # Object of the standard template for communication through ACL messages
    # TODO finalizar con el plantilla estandar final decidida para la comunicacion entre agentes
    STANDARD_ACL_TEMPLATE = Template()
    STANDARD_ACL_TEMPLATE.set_metadata("performative", "CallForProposal")
    # STANDARD_ACL_TEMPLATE.set_metadata("performative", "inform")
    # STANDARD_ACL_TEMPLATE.set_metadata("ontology", "Information")
    # STANDARD_ACL_TEMPLATE.set_metadata("...", "...")
