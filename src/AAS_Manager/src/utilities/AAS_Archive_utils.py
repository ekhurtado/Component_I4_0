# File to save useful methods for accessing the AAS Archive
import calendar
from configparser import ConfigParser
from datetime import datetime
import json
import os
import time

from utilities.AASarchiveInfo import AASarchiveInfo

# svcRequests = "/aas_archive/interactions/ManagerToCore.json"
# svcResponses = "/aas_archive/interactions/CoreToManager.json"
# logFilePath = "/aas_archive/log/ServiceHistory.log"
#
#
# assetRelatedSvcPath = '/aas_archive/services/assetRelatedSvc'
# aasInfrastructureSvcPath = '/aas_archive/services/aasInfrastructureSvc'
# aasServicesPath = '/aas_archive/services/aasServices'
# submodelServicesPath = '/aas_archive/services/submodelServices'

# ------------------------
# Methods related to files
# ------------------------
def createStatusFile():
    """This method creates the status file of the AAS Manager and sets it to "initializing"."""
    config = ConfigParser()
    config['DEFAULT'] = {'name': 'AAS_Manager', 'status': 'Initializing', 'timestamp': str(calendar.timegm(time.gmtime()))}
    with (open(AASarchiveInfo.statusFilePath, 'x') as statusFile):
        config.write(statusFile)
        statusFile.close()

def createInteractionFiles():
    """This method creates the necessary interaction files to exchange information between AAS Core and AAS Manager."""

    # First the service folder is created
    # os.mkdir(AASarchiveInfo.svcFolderPath)

    # The folders for all type of services is also created
    os.mkdir(AASarchiveInfo.assetRelatedSvcPath)
    os.mkdir(AASarchiveInfo.aasInfrastructureSvcPath)
    os.mkdir(AASarchiveInfo.aasServicesPath)
    os.mkdir(AASarchiveInfo.submodelServicesPath)

    # Interaction folders should also be created
    os.mkdir(AASarchiveInfo.assetRelatedSvcPath + '/interactions')
    os.mkdir(AASarchiveInfo.aasInfrastructureSvcPath + '/interactions')
    os.mkdir(AASarchiveInfo.aasServicesPath + '/interactions')
    os.mkdir(AASarchiveInfo.submodelServicesPath + '/interactions')

    # Then the interaction files are added in each folder
    allSvcFolderPaths = [AASarchiveInfo.assetRelatedSvcPath, AASarchiveInfo.aasInfrastructureSvcPath,
                         AASarchiveInfo.aasServicesPath, AASarchiveInfo.submodelServicesPath]
    for svcFolder in allSvcFolderPaths:
        with (open(svcFolder + AASarchiveInfo.svcRequestFileSubPath, 'x') as requestsFile,
              open(svcFolder + AASarchiveInfo.svcResponseFileSubPath, 'x') as responsesFile):
            requestsFile.write('{"serviceRequests": []}')
            responsesFile.write('{"serviceResponses": []}')

            requestsFile.close()
            responsesFile.close()

def createLogFiles():
    """This method creates the necessary log files to save services information."""

    # First the log folder is created
    os.mkdir(AASarchiveInfo.logFolderPath)
    # The folder for services log is also created
    os.mkdir(AASarchiveInfo.svcLogFolderPath)

    # Then the log files are added in each folder
    allSvcLogFileNames = [AASarchiveInfo.assetRelatedSvcLogFileName, AASarchiveInfo.aasInfrastructureSvcLogFileName,
                          AASarchiveInfo.aasServicesLogFileName, AASarchiveInfo.submodelServicesLogFileName]
    for logFileName in allSvcLogFileNames:
        with open(AASarchiveInfo.svcLogFolderPath + '/' + logFileName, 'x') as logFile:
            logFile.write('[]')
            logFile.close()


def fileToJSON(filePath):
    """This method gets the content of a JSON file."""
    f = open(filePath)
    try:
        content = json.load(f)
        f.close()
    except json.JSONDecodeError as e:
        print("Invalid JSON syntax:", e)
        return None
    return content


def updateFile(filePath, content):
    """This method updates the content of a JSON file."""
    with open(filePath, "w") as outfile:
        json.dump(content, outfile)

def XMLToFile(filePath, XML_content):
    """This method writes the content of a XML in a file."""
    with open(filePath, 'wb') as sm_file:
        sm_file.write(XML_content)


# ---------------------------
# Methods related to requests
# ---------------------------
def createSvcRequestJSON(interactionID, svcID, svcType, svcData):
    """This method creates a service request JSON object.

    Parameters
    ----------
    :param interactionID: Identifier of the interaction.
    :param svcID: Identifier of the service
    :param svcType: Type of the service.
    :param svcData: Data of the service in JSON format.

    Returns
    -------
    :return svcRequestJSON: a JSON object with the service request information.
    """
    svcRequestJSON = {"interactionID": interactionID,
                      "serviceID": svcID,
                      "serviceType": svcType,
                      "serviceData": svcData
                      }
    svcRequestJSON['serviceData']['timestamp'] = calendar.timegm(time.gmtime())
    return svcRequestJSON


def addNewSvcRequest(svcTypeFolderPath, newRequestJSON):
    """This method adds a new service request to the related service interaction file and updates it in the AAS Archive.

    Parameters
    ----------
    :param svcTypeFolderPath: The path of the service type folder.
    :param newRequestJSON: The service requests content in JSON format.
    """

    # Get the content of the service requests interaction file
    svcRequestsFilePath = svcTypeFolderPath + AASarchiveInfo.svcRequestFileSubPath
    svcRequestsJSON = fileToJSON(svcRequestsFilePath)
    if svcRequestsJSON is None:
        svcRequestsJSON = {'serviceRequests': [newRequestJSON]}
    else:
        svcRequestsJSON['serviceRequests'].append(newRequestJSON)

    updateFile(svcRequestsFilePath, svcRequestsJSON)

def getSvcRequestInfo(svcTypeFolderPath, interactionID):
    """This method gets the information of a service request.

    Parameters
    ----------
    :param svcTypeFolderPath: The path of the service type folder.
    :param interactionID: Identifier of the interaction.

    Returns
    -------
    :return the information of the service request in JSON format.
    """
    svcRequestsJSON = fileToJSON(svcTypeFolderPath + AASarchiveInfo.svcRequestFileSubPath)
    for i in svcRequestsJSON['serviceRequests']:
        if i['interactionID'] == interactionID:
            return i
    return None

# ----------------------------
# Methods related to responses
# ----------------------------
def getSvcResponse(svcTypeFolderPath, interactionID):
    """This method gets the information of a service request.

    Parameters
    ----------
    :param svcTypeFolderPath: The path of the service type folder.
    :param interactionID: Identifier of the interaction.

    Returns
    -------
    :return the information of the service request in JSON format.
    """
    svcResponsesJSON = fileToJSON(svcTypeFolderPath + AASarchiveInfo.svcResponseFileSubPath)
    for i in svcResponsesJSON['serviceResponses']:
        if i['interactionID'] == interactionID:
            return i
    return None

# ----------------------------
# Methods related to responses
# ----------------------------
def saveSvcInfoInLogFile(svcTypeInteractionPath, svcTypeLogFileName, interactionID):
    """This method saves the information of a service request in the associated log file.

    Parameters
    ----------
    :param svcTypeInteractionPath: The path to the interaction folder of the service.
    :param svcTypeLogFileName: The log file name of the service type.
    :param interactionID: Identifier of the interaction.
    """

    # Get the information about the request and response
    svcResponseInfo = getSvcResponse(svcTypeInteractionPath, interactionID)
    svcRequestInfo = getSvcRequestInfo(svcTypeInteractionPath, interactionID)

    # Create the JSON structure
    logStructure = {
        'level': 'INFO',
        'interactionID': interactionID,
        'serviceStatus': svcResponseInfo['serviceStatus'],
        'serviceInfo': {
            'serviceID': svcRequestInfo['serviceID'],
            'serviceType': svcRequestInfo['serviceType'],
            'requestTimestamp': str(datetime.fromtimestamp(svcRequestInfo['serviceData']['timestamp'])),
            'responseTimestamp': str(datetime.fromtimestamp(svcResponseInfo['serviceData']['timestamp']))
        }
    }
    # If some data has been requested, added to the structura
    requestedData = svcRequestInfo['serviceData']['requestedData']
    if requestedData is not None:
        svcDataJSON = {'requestedData': requestedData, 'dataValue': svcResponseInfo['serviceData'][requestedData]}
        logStructure['serviceInfo']['serviceData'] = svcDataJSON

    # Get the content of LOG file
    logFileJSON = fileToJSON(AASarchiveInfo.svcLogFolderPath + '/' + svcTypeLogFileName)

    # Add the structure in the file
    logFileJSON.append(logStructure)
    updateFile(filePath=AASarchiveInfo.svcLogFolderPath + '/' + svcTypeLogFileName, content=logFileJSON)
    print("Service information related to interaction " + str(interactionID) + " added in log file.")