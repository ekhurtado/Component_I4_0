import logging

from utilities.AASarchiveInfo import AASarchiveInfo


class GeneralUtils:
    """
    This class contains some general utils to ben used by any module.
    """

    @staticmethod
    def configure_logging():
        """
        This method configures the logging to be used by all modules.
        """

        logging.basicConfig(
            level=logging.INFO,
            format="\x1b[36;20m%(asctime)s [%(name)s] [%(levelname)s] %(message)s\x1b[0m",
            handlers=[
                # logging.FileHandler(AASarchiveInfo.LOG_FOLDER_PATH + '/' + AASarchiveInfo.AAS_MANAGER_LOG_FILENAME),
                logging.FileHandler(AASarchiveInfo.AAS_MANAGER_LOG_FILENAME),  # For testing
                logging.StreamHandler()
            ]
        )

        # Set red color for error messages
        errorConsole = logging.StreamHandler()
        errorConsole.setLevel(logging.ERROR)
        formatter = logging.Formatter('\x1b[31;20m%(asctime)s [%(name)s] [%(levelname)s] %(message)s line:%(lineno)d\x1b[0m')
        errorConsole.setFormatter(formatter)
        logging.getLogger('').addHandler(errorConsole)
