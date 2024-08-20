import os
import logging
from msfabricpysdkcore import FabricClientCore

# TODO: new workspaces from branch out do not inherit ownership, so we need to add a tech user as on of the members of the workspace

def prepare_authentication():
    # TODO for Fabric Product Group: move this to service principal auth and remove the username and password
    # https://news.microsoft.com/features/whats-solution-growing-problem-passwords-says-microsoft/
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

target_ws_name = "Fabric_CICD_demo"
target_ws = fc.get_workspace_by_name(target_ws_name)
target_lh = target_ws.list_lakehouses(with_properties=True)[0]  # assume there is only one lakehouse

for source_ws in wss:
    # if name start with Fabric_CICD_demo_
    if source_ws.display_name.startswith(target_ws_name + "_"):
        source_lh = source_ws.list_lakehouses(with_properties=True)[0]  # assume there is only one lakehouse
        for table in target_lh.list_tables(): # TODO for Fabric Product Group: fix for Lakehouses with schema enabled
            try:
                source_lh.create_shortcut(
                    path="Tables",
                    name=table["name"],
                    target={
                        "oneLake": {
                            "itemId": target_lh.id,
                            "path": "Tables/" + table["name"],
                            "workspaceId": target_ws.id
                        }
                    }
                )
            except Exception as e:
                expected_error = '"errorCode":"Copy, Rename or Update of shortcuts are not supported by OneLake."'
                if expected_error in e.args[0]:
                    logger.warning("Shortcut already exists, skipping")
                else:
                    raise e

print("Done")