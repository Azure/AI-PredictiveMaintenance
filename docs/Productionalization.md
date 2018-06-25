# Objectives
The purpose of this document is to first define the basics of operating a production solution in Azure, provide references to the best practices documents for each of those concepts, then describe how those concepts should be applied to each component of a Predictive Maintenance solution.
# Definitions and best practices
## Source control
[Visual Studio Team Services (VSTS)](https://docs.microsoft.com/en-us/vsts/index?view=vsts) provides a [new user guide](https://docs.microsoft.com/en-us/vsts/user-guide/?view=vsts) to get started with VSTS and Git.
## Infrastructure as code (IaC)
This solution template includes a set of Azure Resource Manager (ARM) templates to provision Azure resources for the PdM demo scenario.  As you modify and extend the solution to meet your production needs, modeling your own infrastructure as code will avoid environment drift between your testing, qualification, and production environments.  You can leverage [Microsoft's best practices for infrastructure as code](https://docs.microsoft.com/en-us/azure/devops/what-is-infrastructure-as-code).
## Environments - Dev-test and production
In order to reduce the risk of promoting code into production, the best practices guidance from Azure is to create isolated environments to enable development, quality assurance (QA), and production.  You can leverage the reference architecture guides for [Platform as a Service (PaaS)](https://azure.microsoft.com/en-us/solutions/architecture/dev-test-paas/) and [microservices](https://azure.microsoft.com/en-us/solutions/architecture/dev-test-microservice/).
## Continuous integration and continuous delivery - CICD
Replacing manual gates between environments with automation accelerates delivery of changes to production.  You can leverage Microsoft's architecture guides with [CICD for webapps](https://azure.microsoft.com/en-us/solutions/architecture/vsts-continuous-integration-and-continuous-deployment-for-azure-web-apps/) and [CICD for containers](https://azure.microsoft.com/en-us/solutions/architecture/cicd-for-containers/).
## Application monitoring
[Azure Application Insights](https://docs.microsoft.com/en-us/azure/application-insights/) is the Microsoft Azure best practice for monitoring your application performance.  [Azure Monitor](https://docs.microsoft.com/en-us/azure/monitoring/) is the Microsoft Azure best practice for monitoring your application infrastructure.

# Data collection
## Machine manufacturer telemetry collection guidance
For each unique machine type that you will be operating and monitoring, you need to ensure that you have adequate data collection components in place to inform your prediction system.  This starts first by following the manufacturer guidance to instrument your machine with the appropriate sensors, then collecting and storing that data during operation.
## Real time data ingress: IoT hub, scale, security
The implementation details of real-time ingress are documented in the [data collection section of the solution design document](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Solution-Design.md#i-data-collection).  Azure IoT Hub is designed to handle scalablility and security out of the box.  If you are collecting your real-time telemetry with another service, you will need to include your own answers to scalability and security.
## Long term storage of live data - blob storage (archive), table storage, security
Training and retraining requires a long time period of historical data.  IoT Hub natively supports routing messages to Azure storage as BLOBs.  If you are collecting your real-time telemetry with another service, you will need to include a long term persistance story.
## Maintenance records
As the data accumulates over time, you will need to store records for each maintenance event, planned and unplanned, in a data store.
## Augmentation with recommended maintenance schedule and manufacturer reference data
In order to produce useful predictions from your model you will need to have a sufficient depth and breadth of training data.  This may not be possible if you are operating a small number of machines, or if you have been operating your machines for a short period of time, or if you have very few failure instances.  You can overcome this gap by augmenting your data with reference data from your machine manufacturer.  However, if the manufacturer does not have reference data, you can model your system with rules-based failure prediction based on the maintenance schedule.

# Modeling
## Small scale modeling on the DSVM
## Large scale modeling featurization - Infrastructure guidance, on-demand cluster provisioning, data pump, velocity monitoring
## Large scale model training - Infrastructure guidance, on-demand cluster provisioning, data pump, velocity monitoring
## Model accuracy
## Model management

# Scoring pipeline
## Real time featurization - Infrastructure guidance, scale, security, CICD, monitoring, logging, alerting, defect root cause
## Storing featurized data - featurizer version, cluster id, node id, long term storage, security, auditability
## Real time scoring - Infrastructure guidance (ACI, AKS), scale, security, CICD, monitoring, logging, alerting, defect root cause
## Storing scored data - scorer version, cluster id, node id, long term storage, security, auditability
## Presentation of predictions
## Consumption of predictions
