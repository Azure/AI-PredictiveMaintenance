# PdM Solution Template Architecture

PdM solution deployments are observed in three scenarios:

- _Cloud-based_: Devices are managed from the cloud from a cloud-based service such as the IoT Hub. Device data is delivered via SSL into the cloud. AI and analytics processing is centralized in the cloud. Model train-test and operationalization are done in the cloud.
- _Edge based_: Model train-test is done centrally in the cloud, but the finished models are operationalized on edge devices. [Azure IoT Edge](https://azure.microsoft.com/en-us/services/iot-edge/) supports this scenario.
- _On Prem_: For various reasons, customers may require the PdM application to be on-prem. Devices are not connected to the cloud, but deliver sensor data via local networks to on-prem servers for data and analytics. Device management, collection of maintenance logs, and device meta is handled in local servers. [Microsoft SQL Server Machine Learning Services](https://docs.microsoft.com/en-us/sql/advanced-analytics/what-is-sql-server-machine-learning?view=sql-server-2017) supports this scenario.
- _Cloud On-Prem_: [Azure Stack](https://azure.microsoft.com/en-us/overview/azure-stack/) is a potential target in the future, and not in scope for this discussion. 

This solution template provides an architecture that supports _cloud based_ scenarios. Conceptually, production AI applications are composed of two operational parts:
- an _inner experimentation loop_ that iteratively performs feature engineering, model training and validation, and manages candidate models to be operationalized.
- an _outer processing pipeline_ that handles the inputs to, and outputs from, this inner experimentation loop. On the input side, it handles data ingestion, staging, and preparation. On the output side, it handles model operationalization, publishing, and presentation of results. Requirements for scale, security, availability, and manageability are handled by this outer processing pipeline.

[//]: # (**ONCE THE AI GUIDE IS IN MICROSOFT DOCS, UPDATE THE LINKS BELOW TO HTTP ADDRESS**)

This template demonstrates how to build an end to end POC solution composed of these two parts. Review this architecture along with the [Azure AI Guide to Predictive Maintenance](.\cortana-analytics-playbook-predictive-maintenance.md) as a reference.

## How it works - in a Nutshell 

![PdM_Solution_Template](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/PdM_Solution_Template.png)

Figure 1. PdM solution template architecture

The diagram shows the Azure services that are deployed into the specified resource group. It also shows the data and control flow between these different components during usage. A step by step walkthrough of the architecture follows.

GENERATE

**1:** The data generator deployed with the template helps emulate real-time data generation for a (hypothetical) customer scenario. Tens to hundreds of devices can be registered with an IoTHub. Each device can have multiple sensors for attributes such as temperature, pressure etc. Each sensor can be calibrated to produce output at a specific frequency and amplitude.

INGEST

**2:** Azure IoT Hub is a fully managed service that enables reliable and secure bidirectional communications between millions of IoT devices and a solution back end. Device data streamed out of the IoT Hub is staged in Azure Storage Blobs.

**3:** Maintenance logs, error logs, and failure history that are stored in historical databases at the (hypothetical) customer premise are loaded into Azure Storage Blobs. The storage account provides a repository for other generated artifacts that need to survive across resource deletions or reconfigurations. Specific examples:
- Notebooks for use cases.
- Pickled (.zip) model files generated as a result of modeling experiments.
- Stationary training, test and new data to be scored. Stationary data is typical in most PdM applications.

PREPARE

Data preparation is done in combination with feature engineering as part of the next step.

TRAIN-TEST

**4:** The Train-Test phase is an iterative experimental process to create models that meet the required success criteria. A DSVM is provisioned in the resource group as the developer's workbench. The Jupyter notebook runtime installed in DSVM supports multiple [iPython kernels](http://jupyter.readthedocs.io/en/latest/projects/kernels.html).
- For moderately sized training datasets (MB to few GB), train and test routines can be run against a local Python runtime, or locally provisioned Spark clusters (this example is shown with Use Case 2).
- For larger datasets, the user can provision [Azure HDInsight](https://azure.microsoft.com/en-us/services/hdinsight/) from the Admin dashboard (see [Solution Template Deployment - step by step](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Deployment.md)). By switching the iPython kernel to HDInsight, the user can run the notebooks on the HDInsight Spark clusters.

**5:** Once the models are created, the pickle files of the models are maintained in Blob storage. Accidental loss of models owing to cluster or DSVM deletion is prevented in this manner.

OPERATIONALIZE

**6:** The pickled files representing the models are registered with Azure MLv2.0 model management service along with relevant metadata. Once Azure MLv2.0 is generally available, the duplication of model files may no longer be necessary.

**7:** Azure MLv2.0 is then used to deploy the models for online scoring.

**8:** Data from Azure Blobs is preprocessed and written into a service bus to sequence messages correctly.
- Use Case 1 demonstrates online scoring. Two web jobs are used in this implementation, The first web job fetches a new record from the service bus, and provides it to the second web job. The second web job generates the prediction for this record. Docker images hosting these two web jobs are run on a Kubernetes cluster. Each of the Docker image has its own Spark cluster.

The Spark runtime enables the PySpark routines to preprocess and feature engineer the scoring data using the same steps as that of the training data. For online scoring, each new record is scored. Batch scoring is emulated by grouping together new data rows in small batches of ten or twenty and scoring the output.

PUBLISH

**9:** Predictions are written into Azure Storage tables. 

CONSUME

A PowerBI or other BI client can be used for data visualization. This implementation is not in scope for this template.

## System Design

**TBD - Basic design document in 3-4 paragraphs**

## Solution Template Source Code Explained

The Python code for the inner experimentation loop for model train-test and validation is discussed here:
- [Model train and test - by use case](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Model-Train-Test.md)
- [Model operationalization - by use case](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Model-Operationalize.md)

The code used to implement the outer processing pipeline is described below.

| Stage | File under $GITHUBROOT | Purpose |
|------------------------|-------|---------|
| Deployment | assets\\* | TBD |
| Deployment | core\Manifest.xml  | TBD |
| Deployment | core\markdown\Instructions.md | TBD |
| Deployment | core\arm\*.json | JSON specification of component ARM templates |
| TBD | src\build.proj | TBD |
| TBD | src\AML\aml_config\\* | TBD |
| TBD | src\AML\aml_config\Notebooks | Notebooks by Use Case |
| TBD | src\AML\aml_config\Notebooks\.pynb_checkpoints | TBD |
| TBD | src\WebApp\blankArmTemplate.json | TBD |
| TBD | src\WebApp\requirements.txt | TBD |
| TBD | src\WebApp\setup.html | TBD |
| TBD | src\WebApp\setup.js | TBD |
| TBD | src\WebApp\setup.ps1 | TBD |
| TBD | src\WebApp\web.config | TBD |
| Generate  | src\WebApp\App_Data\jobs\continuous\Simulator\simulator.py | TBD |
| Generate  | src\WebApp\App_Data\jobs\continuous\DataSync\run.cmd | TBD |
| Generate  | src\WebApp\App_Data\jobs\continuous\DataSync\settings.job | TBD |
| Generate  | src\WebApp\App_Data\jobs\continuous\DataSync\sync.py | TBD |
| TBD | src\WebApp\flask\README.md | TBD
| TBD | src\WebApp\flask\app.py | TBD |
| Operationalize | src\WebApp\flask\model_management.py | TBD |
| Operationalize | src\WebApp\flask\aztk_cluster.py | TBD |
| TBD | src\WebApp\flask\spark\customScripts\jupyter.sh | TBD |
| TBD | src\WebApp\flask\spark\spark\.config\core-site.xml | TBD |
| TBD | src\WebApp\flask\spark\spark\.config\spark-defaults.xml | TBD |
| TBD | src\WebApp\flask\spark\spark\.config\spark-env.sh | TBD |
| TBD | src\WebApp\flask\static\\* | Decorative .png files used in Notebooks |
| Dashboard | src\WebApp\flask\templates\\*.html | HTML for Dashboard UX |
| Documentation | README.md | Home Page |
| Documentation | LICENSE | Text for Creative Commons License |
| Documentation | LICENSE_CODE | Text for MIT License |
| Documentation | docs\Architecture.md | Solution Template Architecture description - this file |
| Documentation | docs\Deployment.md | Step by step deployment walkthrough |
| Documentation | docs\Model-Train-and-Test.md | Train and Test descriptions for each use case |
| Documentation | docs\Model-operationalize.md | Operationalization description by use case |
| Documentation | docs\Developers-Guide.md | Guidelines to adapt the template for new scenarios |
| Documentation | docs\FAQ.md | Frequently asked questions about the architecture |
| Documentation | docs\Release-Notes.md | Notes on updates, known bugs and mitigations |
| Documentation | docs\AZTK-instructions.md | TBD |
| Documentation | docs\img\\* | Images used in documentation |
| Documentation | docs\media\cortana-analytics-playbook-predictive-maintenance\\* | _TEMPORARY - images for local copy of Azure AI Guide for Predictive Maintenance_ |
| Documentation | docs\cortana-analytics-playbook-predictive-maintenance.md | _TEMPORARY - Local copy of Azure AI Guide for Predictive Maintenance. This will be removed once the main document is reviewed and submitted into Microsoft Docs_ |
