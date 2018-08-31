# Developers' Manual

This document describes implementation specifics of the solution.

## Deployment mechanism

Solution's resources are created through deployments of multiple Azure Resource Manager (ARM) [templates](../src/ARMTemplates), which are linked together by [pdm-arm.json](../src/ARMTemplates/pdm-arm.json). (Linked templates are covered in great detail in [this article](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-linked-templates).)

If you wish to customize this solution by cloning this GitHub repository, be sure to update the ```gitHubBaseUrl``` variable accordingly in the [main ARM template](../src/ARMTemplates/pdm-arm.json#L60) so that it points to your clone repository.

The ARM templates can also be reused outside of GitHub, which would require deploying them in a certain order such that resource and input/output parameter dependencies are maintained.

### Additional deployment components

In addition to the ARM deployments, the solution depends on custom several custom configuration activities implemented as WebJobs:

1. [Python and storage setup](../src/WebApp/App_Data/jobs/continuous/PythonAndStorageSetup), which configures Python 3.6 runtimes and creates several storage tables used by the solution
2. [Databricks and simulated devices setup](../src/WebApp/App_Data/jobs/continuous/DatabricksAndSimulatedDevicesSetup), which creates a databricks cluster used for real-time feature engineering as well as several "test" IoT devices used by the data generator.

These Web Jobs are implemented as "continuous," despite the fact that they need to run only once. Please refer to the source code for more details.

## Data generator



## Feature engineering and scoring pipeline

## Futher steps
