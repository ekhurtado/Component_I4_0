import logging
from spade.behaviour import State

from behaviours.ACLHandlingBehaviour import ACLHandlingBehaviour
from utilities import AAS_Archive_utils
from utilities.AASmanagerInfo import AASmanagerInfo

_logger = logging.getLogger(__name__)


class StateRunning(State):
    """
    This class contains the Running state of the common AAS Manager.
    """

    async def run(self):
        """
        This method implements the running state of the common AAS Manager. Here all requests services are handled,
        both from ACL of another AAS Manager or from the AAS Core.
        """

        _logger.info("## STATE 2: RUNNING ##  (Initial state)")

        # IAAS Manager is in the Running status
        AAS_Archive_utils.change_status('Running')

        # On the one hand, a behaviour is required to handle ACL message
        acl_handling_behav = ACLHandlingBehaviour(self.agent)
        self.agent.add_behaviour(acl_handling_behav, AASmanagerInfo.STANDARD_ACL_TEMPLATE)

        # Wait until the behaviour has finished. Is a CyclicBehaviour, so it will not end until an error occurs or, if
        # desired, it can be terminated manually using "behaviour.kill()".
        await acl_handling_behav.join()

        # If the Execution Running State has been completed, the agent can move to the next state
        _logger.info(f"{self.agent.jid} agent has finished it Running state.")
        self.set_next_state(AASmanagerInfo.STOPPING_STATE_NAME)
