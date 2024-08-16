# Introduction 
The target of this repo is to interact with the Fabric Rest API in Azure DevOps Pipelines to build automation and CICD, e.g. creating shortcuts to original workspace lakehouse after branching into new workspace. 
Because currently [Service Principal Auth](https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-shortcuts/create-shortcut?tabs=HTTP) is not supported in a lot of APIs we use the following workaround (which will need to be discussed with your security team):
  1. Create a regular Entra ID User
  1. Exclude the user from two factor auth policies of your tenant
  1. Include the user into a location based conditional access policy that allows the user to login with user and password only from a specifc IP range (in this case the self hosted devops agent pool)
  1. Give the user the right for the workspaces to manage, e.g. member
  1. Build a devops yaml pipeline:
     1. use [azure-cli](https://pypi.org/project/azure-cli/) in python to run `az login` for user and password auth
     1. use [msfabriccoresdk](https://pypi.org/project/msfabricpysdkcore/) for interaction with the APIs in python
        1. create shortcut / do your CICD stuff

We know this is not yet inline with Microsofts approach to security:
https://news.microsoft.com/features/whats-solution-growing-problem-passwords-says-microsoft/
But it is a solution that can be discussed with your central cloud governance team.
It relies on proper use of conditional access which is the way forward in a ZeroTrust World anyways.