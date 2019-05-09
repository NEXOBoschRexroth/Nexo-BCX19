# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import sys
import json
import os
import threading
# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=Nexo.azure-devices.net;DeviceId=SvenTest;SharedAccessKey=j/jTPMXwNYmDtcsw93YfuWWPar5MKWBDfOQvCnqql3I="
CONNECTION_STRING = "HostName=neptun.azure-devices.net;DeviceId=nepson;SharedAccessKey=bRJHpoDTV7S7H6Usjc2Ng6Fe0/Kqkw+LLyY/dxN4zpY="


# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000



FTP_DIR = r"/home/ftp"

SENDING_FILES = []
lock = threading.Lock()

def send_confirmation_callback(message, result, user_context):
    
    lock.acquire()
    print ( "IoT Hub responded to message with status: %s" % (result) )
    print (user_context)
    filePath = user_context
    os.remove(filePath)
    SENDING_FILES.remove(filePath)
    lock.release()
    
    
def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def iothub_client_telemetry_run():
    
    
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
      
            # Build the message with simulated telemetry values.
            for root, dirs, files in os.walk(FTP_DIR):
                for file in files:
            
                    filePath = os.path.join(root, file)
                    print SENDING_FILES
                    
                    lock.acquire()
                    if filePath in SENDING_FILES:
                        continue
                    lock.release()
                    
                    try:
                        with open(filePath, "r") as json_file:  
                            data = json.load(json_file)
                            stringData = json.dumps(data)
    
                    except (ValueError, IOError) as e:
    
                        time.sleep(0.1)
                        continue
                    
                    
                    message = IoTHubMessage(stringData)
                    
                    # Send the message.
                    print( "Sending message: %s" % message.get_string() )
                    
                    lock.acquire()
                    SENDING_FILES.append(filePath)
                    lock.release()
                    
                    client.send_event_async(message, send_confirmation_callback, filePath)
                    
                    time.sleep(0.5)
                    
                    
                
    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
    
   
if __name__ == '__main__':
    print ( "IoT Hub - NEXO FTP" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_run()