# Objectives
The purpose of this document is to define the basics of operating a production solution in Azure, provide references to the best practices documents for each of those concepts, then describe how those concepts should be applied to each component of a Predictive Maintenance solution.



# Data collection
## Real time data ingress: IoT hub, scale, security
The implementation details of real-time ingress are documented in the [data collection section of the solution design document](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Solution-Design.md#i-data-collection).  Azure IoT Hub is designed to handle scalablility and security out of the box.  Refer to the [IoT Solutions Remote Monitoring documentation](https://docs.microsoft.com/en-us/azure/iot-accelerators/iot-accelerators-remote-monitoring-explore) for details.  If you are collecting your real-time telemetry with another service, you will need to include your own answers to scalability and security.  Attempting to solve a predictive maintenance problem is predicated on already having a comprehensive remote monitoring solution operationalized.

# Modeling
## Featurization
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
## Model training
TODO
## Model management
Refer to [the authoritative model management documentation](https://docs.microsoft.com/en-us/azure/machine-learning/desktop-workbench/model-management-overview) produced by the Azure Machine Learning Model Management team.
## Model operationalization
TODO

# Scoring
## Real-time featurization
### Scalability points (with respect to telemetry frequency and the number of machines, and – perhaps – the type of telemetry)
IoT Hub
Spark cluster
Running featurization in Streaming mode vs semi-batch mode (this needs to cover EventHub’s data retention policy)
### Recovery from failures (what to do if the featurizer crashes?)
[Azure Application Insights](https://docs.microsoft.com/en-us/azure/application-insights/) is the Microsoft Azure best practice for monitoring your application performance.  [Azure Monitor](https://docs.microsoft.com/en-us/azure/monitoring/) is the Microsoft Azure best practice for monitoring your application infrastructure.

### Cost
## Real-time scoring
### Application containers - ACI vs AKS (vs other)
### Cost
## Visualization and actions
* Power BI
* Custom dashboards
* Remote Monitoring

