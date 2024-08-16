import os
import logging
from msfabricpysdkcore import FabricClientCore

def prepare_authentication():
    ## TODO: move this to service principal auth and remove the username and password
    # get username and password from environment variables
    username = os.environ.get('FABRIC_USERNAME')
    password = os.environ.get('FABRIC_PASSWORD')

    cmd = f"az login --allow-no-subscriptions --username {username} --password {password}"
    # execute python in command line
    os.system(cmd)

prepare_authentication()

logger = logging.getLogger(__name__)
fc = FabricClientCore()
wss = fc.list_workspaces()
logger.info(wss)
print(wss)