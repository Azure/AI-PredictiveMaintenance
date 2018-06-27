# Objectives
The purpose of this document is to provide guidance for you to configure each component of your Predictive Maintenance solution for handling production workloads.

# Data collection
## Real time data ingress with IoT Hub
The implementation details of real-time ingress are documented in the [data collection section of the solution design document](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Solution-Design.md#i-data-collection).

Azure IoT Hub offers several options based on [pricing](https://azure.microsoft.com/en-us/pricing/details/iot-hub/) and [scale](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-scaling).  IoT Hub provides [basic and standard tiers](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-scaling#basic-and-standard-tiers) which will impact the features available.  Both tiers provide the same [3 options for throughput scale](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-scaling#message-throughput).

Refer to the [IoT Solutions Remote Monitoring documentation](https://docs.microsoft.com/en-us/azure/iot-accelerators/iot-accelerators-remote-monitoring-explore) for details.  Attempting to solve a predictive maintenance problem is predicated on already having a comprehensive remote monitoring solution operationalized.

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
## Model management and operationalization
Refer to [the authoritative model management documentation](https://docs.microsoft.com/en-us/azure/machine-learning/desktop-workbench/model-management-overview) produced by the Azure Machine Learning Model Management team.

# Scoring
## Real-time featurization
### Scalability points (with respect to telemetry frequency and the number of machines, and – perhaps – the type of telemetry)
* Spark cluster
* Running featurization in Streaming mode vs semi-batch mode (this needs to cover EventHub’s data retention policy)
### Recovery from failures (what to do if the featurizer crashes?)
[Azure Application Insights](https://docs.microsoft.com/en-us/azure/application-insights/) is the Microsoft Azure best practice for monitoring your application performance.  [Azure Monitor](https://docs.microsoft.com/en-us/azure/monitoring/) is the Microsoft Azure best practice for monitoring your application infrastructure.

### Cost
TODO
## Real-time scoring
### Application containers - ACI vs AKS (vs other)
TODO
### Cost
TODO
## Visualization and actions
* Power BI
* Custom dashboards
* Remote Monitoring

