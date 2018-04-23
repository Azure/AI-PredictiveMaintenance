# [Azure AI Predictive Maintenance (PdM) Solution Template](https://github.com/Azure/AI-PredictiveMaintenance)

[![Deploy to Azure](https://raw.githubusercontent.com/Azure/Azure-CortanaIntelligence-SolutionAuthoringWorkspace/master/docs/images/DeployToAzure.PNG)](https://quickstart.azure.ai/Deployments/new/ai-predictivemaintenance)

## <span style="color:red"> PRIVATE PREVIEW
#### Please send your questions, feedback, comments to ciqsoncall@microsoft.com 

## Summary
This solution template provides a proof-of-concept (POC) implementation of an end to end PdM solution template for the scenario: _Predict the probablity that a piece of equipment fails within a future time period_. This scenario takes ideas from the [Predictive Maintenance Playbook (Revised)](./docs/cortana-analytics-playbook-predictive-maintenance.md) - a review of this playbook in conjunction with using this template is highly reocmmended.

The main value prop of this solution template is its implementation of an end to end PdM solution that shows both model creation and operationalization (online scoring of new data) using Azure ML v2.0 (Preview Edition) on scalable Azure cluster services. It also provides a general purpose data generator that can closely mimic data ingestion from live sensors into a IoTHub, a data staging and processing pipeline from the IoTHub; model creation using PySpark on scalable Azure cluster services, model management using Azure ML v2.0 (Preview), and model operationalization on a scalable Azure cluster service using Azure ML v2.0.

You can quickly deploy this template to a resource group in your Azure subscription, and adapt the components in subscription to fit your application needs. Documentation provided with the template explains the scenario, the data science, and the end to end architecture.

### Audience

- If you are a business decision maker (BDM) looking to reduce the downtime and improve utilization of critical equipment, start with the section _Business case for PdM_ in the [PdM Playbook (Revised)](./docs/cortana-analytics-playbook-predictive-maintenance.md).
- If you are a technical decision maker (TDM) trying to understand PdM technologies, the data science behind them, and the path to their implementation, start with _Data Science for PdM_ section in the [PdM Playbook](./docs/cortana-analytics-playbook-predictive-maintenance.md).
- If you are a sofware architect or developer looking to quickly stand up a POC, start with [Solution Template Architecture for PdM](#Solution-Template-Architecture-for-PdM).

### Prerequisites

You will need an [Azure subscription](https://azure.microsoft.com/en-us/pricing/purchase-options/) and [sufficient quota](https://blogs.msdn.microsoft.com/skeeler/2017/01/subscription-usage-and-quotas-in-the-azure-portal/) for the Azure services shown below.

![Resources](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/Resources.png)

### Estimated Cost and Deployment Time

>NOTE: If you have already deployed this solution, click [here](https://start.cortanaintelligence.com/Deployments) to view your deployment.

The daily cost of running this solution template in its default configuration is $20 per day. The deployment of this solution template completes in 90 minutes if all the cluster resources are available; and may take 3 hours to complete if Azure services are under peak loads.

## Solution Template
The rest of the content is organized as follows:

- [Step by Step Deployment Walkthrough](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Deployment-Walkthrough.md)
- [Solution Template Architecture](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Architecture.md)
- [Model creation and operationalization](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Data-Science.md)
- [Frequently Asked Questions](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/FAQ.md)
- [Release Notes and Trouble Shooting Guide](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Release-Notes.md)

## Data/Telemetry
This advance scenarios for General Predictive Maintenance collects usage data and sends it to Microsoft to help improve our products and services. Read our [privacy statement](https://privacy.microsoft.com/en-us/privacystatement) to learn more.

## Contributing
This project welcomes contributions and suggestions. Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot automatically determines whether you need to provide a CLA and decorates the pull request appropriately. You only need to follow the instructions provided by the bot across all Microsoft repositories to use our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). More information is available at Code of Conduct FAQ. Contact opencode@microsoft.com with any additional questions or comments.