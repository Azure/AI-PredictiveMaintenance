# [Azure AI Predictive Maintenance Solution Template](https://github.com/Azure/AI-PredictiveMaintenance)

[![Deploy to Azure](https://raw.githubusercontent.com/Azure/Azure-CortanaIntelligence-SolutionAuthoringWorkspace/master/docs/images/DeployToAzure.PNG)](https://quickstart.azure.ai/Deployments/new/ai-predictivemaintenance)

## Summary

This solution template provides an architectural framework to build proof-of-concept (POC) solutions for Predictive Maintenance (PdM). It shows how to put together an end to end PdM solution. In-depth content on the why and how of the data science and the software design are provided. A key motivation behind this template is to enable developers to quickly reuse or customize it for new customer scenarios.

The key phases of an end to end modeling pipeline are shown: data  ingestion, staging, preparation; feature engineering, model training and validation; model operationalization and output of results. Real-time and stationary data ingestion is supported. Modeling experiments can be run both on a hosting DSVM, or on a scalable Azure service. Online and batch scoring are demonstrated. An easy to use dashboard provides a friendly demo experience, hiding the complexity behind provisioning clusters and other resources.

The AI sections of the template follow the principles and practice described in the popular [Azure AI Guide for Predictive Maintenance](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/cortana-analytics-playbook-predictive-maintenance) (previously called _Cortana Intelligence Predictive Maintenance Playbook for aerospace and other industries_). Two PdM use cases are provided with the template:
1. (Use Case UC1) Predict failure condition of a machine - based on real-time sensor-based data.
2. (Use Case UC2) Predict that a machine will fail within a future time period - based on historical stationary data.

The goal is to demonstrate the use of multiple solutions in the same template. Based on these examples, practitioners can reuse the template for their own customer scenario and data.

The code for the solution template is [available in GitHub](http://github.com/azure/AI-PredictiveMaintenance). Contribution of new PdM solutions built using the template is highly encouraged. Similarly, good quality code that extends the template's architecture for useful scenarios is also welcomed. See the [Contributing](#Contributing) section.

## Audience

| Start with ... | If you are ... |
|:---------------|----------------|
| _Business case for PdM_ section in the [Azure AI Guide for Predictive Maintenance](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/cortana-analytics-playbook-predictive-maintenance) | a business decision maker (BDM) looking to reduce the downtime and improve utilization of critical equipment |
| _Data Science for PdM_ section in the [Azure AI Guide for Predictive Maintenance](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/cortana-analytics-playbook-predictive-maintenance) | a technical decision maker (TDM), architect, or developer, looking to understand the data science behind PdM technologies. |
| This solution template, starting with [Prerequisites](#Prerequisites) | a software architect or developer looking to quickly implement a cloud-based POC solution for Predictive Maintenance with Azure AI. |
| _Solution Templates and Samples for PdM_ in the [Azure AI Guide for Predictive Maintenance](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/cortana-analytics-playbook-predictive-maintenance) | a software architect or developer surveying other technical contributions for predictive maintenance from across Microsoft.

## Prerequisites

### Azure Resources

You will need an [Azure subscription](https://azure.microsoft.com/en-us/pricing/purchase-options/) and [sufficient quota](https://blogs.msdn.microsoft.com/skeeler/2017/01/subscription-usage-and-quotas-in-the-azure-portal/) for the Azure services listed below.

| Name of the service | Type | Purpose in this solution template |
|:--------------------|------|---------|
|[Azure App Service](https://azure.microsoft.com/en-us/services/app-service/) | App Service | the solution template is deployed as an App service |
|[Azure App Services Plan](https://docs.microsoft.com/en-us/azure/app-service/azure-web-sites-web-hosting-plans-in-depth-overview) | App Service plan | same as above |
|[Azure IoT Hub Services](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-what-is-iot-hub) | IoT Hub | management of, and data ingestion from, sensor devices |
|[Azure Blobs & Tables](https://docs.microsoft.com/en-us/azure/storage/common/storage-introduction) | Storage account | Staging of real-time and stationary data |
|[Azure Data Science VM](https://azure.microsoft.com/en-us/services/virtual-machines/data-science-virtual-machines/) | Virtual machine | Workstation/space for the AI Developer |
|[Azure Machine Learning Service](https://docs.microsoft.com/en-us/azure/machine-learning/service/) | Machine Learning Model Management | Enable AI Developer to manage models |
|[Azure Kubernetes Cluster (for O16N)](https://docs.microsoft.com/en-us/azure/aks/intro-kubernetes) | Microsoft.MachineLearningCompute/ operationalizationClusters | To operationalize models from Azure ML |
|[Azure Service Bus](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-fundamentals-hybrid-solutions) | Service Bus | To buffer messages for online scoring |

### Skills
The following skills can be helpful to understand the different parts of the template, and post-deployment customizations:

- Most of the code is in [Python](https://www.python.org/). The data generator setup is in Python. [PySpark](https://spark.apache.org/docs/0.9.0/python-programming-guide.html) is used for data management. [PySpark MLlib](http://spark.apache.org/docs/2.0.0/api/python/pyspark.mllib.html) and [Scikit-learn](http://scikit-learn.org/stable/) packages for Python are used for modeling operations.
- Model management and deployment are done via [Azure ML v2.0 CLI](https://docs.microsoft.com/en-us/azure/machine-learning/desktop-workbench/model-management-cli-reference)
- For understanding the various components of the solution template:
  - The manifest of components and their provisioning sequence is specified in [XML](https://www.w3schools.com/xml/default.asp).
  - Each component is configured declaratively in [JSON](https://www.json.org/) (see [ARM templates](https://www.red-gate.com/simple-talk/cloud/infrastructure-as-a-service/azure-resource-manager-arm-templates/)).
  - Data and modeling operations are performed on [Spark](http://spark.apache.org/) clusters either in the local [DSVM](https://azure.microsoft.com/en-us/services/virtual-machines/data-science-virtual-machines/) or on other Azure clustering services such as [Azure HDInsight](https://azure.microsoft.com/en-us/services/hdinsight/).
  - Knowledge of [Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/intro-kubernetes) and [Docker containers](https://www.docker.com/what-container) is helpful.
  - The Admin dashboard is implemented in [Flask](http://flask.pocoo.org/).

## Deploying the solution template

> NOTE: If this solution template has been deployed, click [here](https://quickstart.azure.ai/Deployments) and refresh the browser to see the latest deployment status.

Click on the **Deploy** button to start a new deployment of the solution template. The deployment completes within an hour if all Azure resources are available in the chosen region. Under peak loads, it may take additional time to complete.

See this [step by step deployment walkthrough](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Deployment.md) for details.

## Estimated cost
In its default configuration and quiescent state, the cost of running the template is less than $50 per day. Actual costs may vary depending on the usage and load on the services.

## Description
The solution template and its operations are described in the following sections.

- [Solution Template Architecture](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Architecture.md)
- [Model train and test - self-documented, and by use case](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Model-Train-Test.md)
- [Model operationalization - self-documented, and by use case](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Model-Operationalize.md)

## Privacy
Usage data is collected to help improve Microsoft products and services. See the [privacy statement](https://privacy.microsoft.com/en-us/privacystatement) to learn more.

## Contributing
This project welcomes contributions and suggestions. The contributor is required to agree to a Contributor License Agreement (CLA). The contributor first declares the right to grant Microsoft the rights to use the contribution. Next, the contributor grants Microsoft the right to use the contribution. For details, visit https://cla.microsoft.com.

For each Git pull request, a CLA-bot automatically determines whether the contributor needs to provide a CLA. The steps in the pull request are specified appropriately. Follow the instructions provided by the bot to use the CLA.
 
This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). More information is available at Code of Conduct FAQ. Contact opencode@microsoft.com with any additional questions or comments.