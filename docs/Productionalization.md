# Objectives
The purpose of this document is to define the basics of operating a production solution in Azure, provide references to the best practices documents for each of those concepts, then describe how those concepts should be applied to each component of a Predictive Maintenance solution.
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
The implementation details of real-time ingress are documented in the [data collection section of the solution design document](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Solution-Design.md#i-data-collection).  Azure IoT Hub is designed to handle scalablility and security out of the box.  Refer to the [IoT Solutions Remote Monitoring documentation](https://docs.microsoft.com/en-us/azure/iot-accelerators/iot-accelerators-remote-monitoring-explore) for details.  If you are collecting your real-time telemetry with another service, you will need to include your own answers to scalability and security.
## Long term storage of live data - blob storage (archive), table storage, security
Training and retraining requires a long time period of historical data.  IoT Hub natively supports routing messages to Azure storage as BLOBs.  If you are collecting your real-time telemetry with another service, you will need to include a long term persistance story.
## Maintenance records
As the data accumulates over time, you will need to store records for each maintenance event, planned and unplanned, in a data store.
## Augmentation with recommended maintenance schedule and manufacturer reference data
In order to produce useful predictions from your model you will need to have a sufficient depth and breadth of training data.  This may not be possible if you are operating a small number of machines, or if you have been operating your machines for a short period of time, or if you have very few failure instances.  You can overcome this gap by augmenting your data with reference data from your machine manufacturer.  However, if the manufacturer does not have reference data, you can model your system with rules-based failure prediction based on the maintenance schedule.

# Modeling
## Small scale modeling on the DSVM
It is important to handle your data securely on the DSVM.  You should first familiarize yourself with the [security best practices for IaaS](https://docs.microsoft.com/en-us/azure/security/azure-security-iaas) and apply the recommendations to your VM as appropriate.  You can monitor your VM security state by installing the [VM Agent](https://docs.microsoft.com/en-us/azure/security-center/security-center-enable-vm-agent) on your DSVM via [Azure Security Center](https://docs.microsoft.com/en-us/azure/security-center/).
## Large scale modeling featurization
The recommended large scale featurization platform is [Databricks](https://docs.microsoft.com/en-us/azure/azure-databricks/).  Familiarize yourself with the [Databricks getting started guide](https://databricks.com/product/getting-started-guide) and the [gentle introduction to Apache Spark on Databricks](https://docs.databricks.com/spark/latest/gentle-introduction/gentle-intro.html).
### Infrastructure guidance
The parameters to consider while provisioning your feature engineering cluster are
*  Memory requirements
*  CPU requirements
*  Disk requirements
*  GPU

The documentation for [pricing details of Databricks node types](https://azure.microsoft.com/en-us/pricing/details/databricks/) and [Azure VM series](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/series/) explains the options available.
### On-demand cluster provisioning
By default, your databricks cluser is provisioned as transient.  If your cluster is idle for 120 minutes then the cluster will be released.  There is no need to retain an idle cluster because you can create a new one in seconds.
### Data pump
TODO - How to connect the source data to the notebooks securely?
### Monitoring
You can [monitor your Spark cluster](https://spark.apache.org/docs/latest/monitoring.html) with the built in [web UI](https://jaceklaskowski.gitbooks.io/mastering-apache-spark/spark-webui.html).
### Security
Databricks ships with [enterprise grade security](https://databricks.com/databricks-enterprise-security) built in.
## Large scale model training - Infrastructure guidance, on-demand cluster provisioning, data pump, velocity monitoring
TODO
## Model accuracy
TODO
## Model management
Refer to [the authoritative model management documentation](https://docs.microsoft.com/en-us/azure/machine-learning/desktop-workbench/model-management-overview) produced by the Azure Machine Learning Model Management team.

# Scoring pipeline
## Real time featurization - Infrastructure guidance, scale, security, CICD, monitoring, logging, alerting, defect root cause
## Storing featurized data - featurizer version, cluster id, node id, long term storage, security, auditability
## Real time scoring - Infrastructure guidance (ACI, AKS), scale, security, CICD, monitoring, logging, alerting, defect root cause
## Storing scored data - scorer version, cluster id, node id, long term storage, security, auditability
## Presentation of predictions
## Consumption of predictions
