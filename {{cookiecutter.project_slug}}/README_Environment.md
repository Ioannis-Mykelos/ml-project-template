# Create & register an Environment.

## How to set up the `.github/workflows/environment.yml` file.

### 1 ) Make sure you have the following secrets created and saved in this GitHub repository:
You have to go to `Settings/Secrets and variables/Actions`. There you have to create the following secrets:
- **RESOURCE_GROUP_NAME** : The resource group name (ex: feedbackanalyzer), search [here](https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups).
 - **WORKSPACE_NAME** : The workspace name (ex: feedabckanalyzer-ws-dev) search [here](https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.MachineLearningServices%2Fworkspaces).
 - **SUBSCRIPTION_ID** : The subscription Id (search in the `Overview` when you select the Resourse group).
 - **TENANT_ID** : The Tenant Id (`nuuday-ai-platform-dev-cccoe-lz` for dev) search [here](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade).
 - **SERVICE_PRINCIPAL** : The service principal for this repository you created. Follow the guide for `dev`: [here](https://github.com/nuuday/ai-platform-doc/blob/main/user_guide/HowToSetupAuthentication.md).
 - **SSH_KEY** : The SSH key for the specific Workspace you are working. Follow the guide [here](https://github.com/nuuday/ai-platform-doc/blob/main/user_guide/HowToSetUpSSHKey.md).
 - **REGISTRY_USERNAME** : Find it in the **Container Registry** for your **Resourse group** [here](https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups). (Left **Access keys** option).
 - **REGISTRY_PASSWORD** : Find it in the **Container Registry** for your **Resourse group** [here](https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups). (Left **Access keys** option).


 ### 2 ) Make sure you create an Environment(s) in this GitHub repository:
 You have to go to `Settings/Environments` and create a new environment:
 Click on:
  - **New Environment** and give the name (for example `dev`).
  - **Configure Environment** and **Save protection Rules**


 ### 3 ) Make sure to create variables for the Environment you created in this GitHub repository:
 You have to go to `Settings/Environments`. There you have to click on the `YourEnvironment` and on the block `Environment variables` you can add a variable.
 There you have to create the following Environment Variables:
  - **AZURE_CONTAINER_REGISTRY_NAME** :  Find it in the **Container Registry** (**Login server** on top right) for your **Resourse group** [here](https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups). It look like `alphanumerical.azurecr.io`.

We are done!!!

**IMPORTANT**
 ### 4 ) Ctreate an Environment manually:
 You have to go to the projects repo, to Actions and run manually the **Build and register an environment in Azure ML Studio** action. This action will create an image in the **Container registry** in your Resource Group.
 - Go to the Enviromnets in your Azure ML Studio.
 - Click on create an environment.
 - Give it a name and a description.
 - Select environment source to **Use existing docker image with optional conda file**.
 - Create your environment.

As a reference you can see the following pictures:
<br/>
	<img src=../images/env.png width="1200" height="600">
<br/>

 **Note:** The **CONTAINER REGISTRY IMAGE PATH** you can find in the  **Resource-Group/Container-registry/Repositories**, and then select the container you created (possibly last container in the list), then click on it and copy paste the reference next to the  **Conda pull** tab (it will look like : `260dc72c91e54e93bedad373d9c31008.azurecr.io/environments/YOUR_REPOS_NAME-env:latest`)

**Note:** How to find the **CONTAINER REGISTRY IMAGE PATH**:
See the pictures below:
<br/>
	<img src=../images/con1.png width="1200" height="600">
<br/>

<br/>
	<img src=../images/con2.png width="1200" height="600">
<br/>

<br/>
	<img src=../images/con3.png width="1200" height="600">
<br/>



