# PdM Solution Template Architecture

PdM solution deployments are observed in three scenarios:

- _On Prem_: Devices are not connected to the cloud, but deliver sensor data via local networks to on-prem servers for data and analytics. Device management, collection of maintenance logs, and device meta is handled in local servers. Customers prefer the PdM application to be on-prem, or cannot choose the cloud platform because of regulatory or other reasons. Devices are managed locally. [Microsoft SQL Server Machine Learning Services](https://docs.microsoft.com/en-us/sql/advanced-analytics/what-is-sql-server-machine-learning?view=sql-server-2017) supports this scenario.
- _Cloud-based_: Devices are managed from the cloud from a cloud-based service such as the IoT Hub. Device data is delivered via SSL into the cloud. AI and analytics processing is centralized in the cloud. Model train-test and operationalization are done in the cloud.
- _Edge based_: Model train-test is done centrally in the cloud, but the finished models are operationalized on edge devices. [Azure IoT Edge](https://azure.microsoft.com/en-us/services/iot-edge/) supports this scenario.

This solution template provides an architecture that supports _cloud based_ scenarios. Conceptually, production AI applications are composed of two operational parts:
- an _inner AI loop_ that iteratively performs feature engineering, model training and validation, and manages candidate models to be operationalized.
- an _outer processing pipeline_ that handles the inputs to, and outputs from, this inner AI loop. On the input side, it handles data ingestion, staging, and preparation. On the output side, it handles model operationalization, publishing, and presentation of results. Enterprise-grade requirements for scale, security, availability, and manageability are handled by this outer processing pipeline.

This template demonstrates how to build an end to end POC solution composed of these two parts. Review this architecture along with the [Azure AI Guide to Predictive Maintenance](.\cortana-analytics-playbook-predictive-maintenance.md) as a reference.

## How it works - in a Nutshell 

![PdM_Solution_Template](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/PdM_Solution_Template.png)

Figure 1. PdM solution template architecture

The diagram shows all the Azure services that are deployed into the specified resource group. It also shows the data and control flow between these different components during usage. A step by step walkthrough of the architecture follows.

#### GENERATE
**Step 1:** The data generator deployed with the template helps emulate real-time data generation for a (hypothetical) customer scenario. Tens to hundreds of devices can be registered with an IoTHub. Each device can have multiple sensors for attributes such as temperature, pressure etc.

#### INGEST
**Step 2:** Azure IoT Hub is a fully managed service that enables reliable and secure bidirectional communications between millions of IoT devices and a solution back end. Device data streamed out of the IoT Hub is staged in <span style="color: blue">Azure Storage Blobs</span>.

**Step 3:** Maintenance logs, error logs, and failure history that are stored in the (hypothetical) customer premise are loaded into Azure Storage Blobs. The storage account provides a repository for other generated artifacts that need to survive across resource deletions or reconfigurations. Specific examples:
- Jupyter Notebooks for the use cases in this template, or BYON (bring your own notebooks) for new use cases.
- Picked (.zip) model files generated as a result of modeling experiments
- Stationary training data that is typical of most PdM applications, and also BYOD (bring your own data) for new scenarios adapted from this template.

#### PREPARE

Data preparation is done in combination with feature engineering as part of the next step.

#### TRAIN-TEST

**Step 4:** The Train-Test phase is an iterative process that proceeds until models that meet the success criteria are created. A <span style="color: blue">DSVM</span> is provisioned in the resource group as the developer's workbench. The Jupyter notebook runtime installed in DSVM supports multiple [iPython kernels](http://jupyter.readthedocs.io/en/latest/projects/kernels.html).
- For moderately sized training datasets (MB to few GB), train and test routines can be run against a local Python runtime, or locally provisioned Spark clusters (this example is shown with Use Case 2).
- For larger datasets, the template provisions on-demand Spark on Docker clusters in Azure using [AZTK](https://github.com/Azure/aztk). The developer has to manually start up the cluster from the Admin dashboard (see [Solution Template Deployment - step by step](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Deployment.md)). The dashboard enables easy startup and shutdown of clusters, hiding the complexity of multiple CLI commands.

**Step 5:** The pickle files of the models, created either in DSVM or the clusters, are maintained in Blob storage.

#### OPERATIONALIZE

**Step 6:** The pickle files representing the models are registered with Azure ML2.0 model management service along with relevant metadata.

**Step 7:** Azure MLv2.0 is then used to deploy the models for online scoring or batch scoring.

**Step 8:** Batch scoring is done on a Spark cluster similar to the one used for model training. The new data is provided from Azure Blob storage. As discussed earlier, the training data goes through data preprocessing and feature engineering steps. The same steps in the same sequence have to be executed on the new scoring data.

**Step 9:** Data from Azure Blobs is preprocessed and written into a service bus to sequence messages correctly. Two web jobs implement online scoring. The first web job fetches a new record from the service bus. The second web job generates the prediction for this record. Docker images hosting these two web jobs are run on a Kubernetes cluster.

#### PUBLISH

**Step 10:** Predictions for each device ID  are written into Azure Storage tables. 

#### CONSUME
A PowerBI or other BI client can be used for data visualization, and is not in scope for this template.

## System Design

**<span style="color: red">TBD - Simple design document in 3-4 paragraphs</span>**

## Source Code Explained

The Python code for the inner AI loop of model train-test and validation is discussed in the Use Cases sections. This section focuses on the code used to implement the outer processing pipeline.

**NOTE - automatically enabled hyperlinks for the code below are not correct. TBD**

| Stage | File under $GITHUBROOT | Purpose |
|------------------------|-------|---------|
| Deployment | assets\* | **TBD** |
| Deployment | core\Manifest.xml  | **TBD** |
| Deployment | core\markdown\Instructions.md | **TBD** |
| Deployment | core\arm\*.json | JSON specification of component ARM templates |
| **TBD** | src\WebApp\blankArmTemplate.json | **TBD** |
| **TBD** | src\WebApp\requirements.txt | **TBD** |
| **TBD** | src\WebApp\setup.html | **TBD** |
| **TBD** | src\WebApp\setup.js | **TBD** |
| **TBD** | src\WebApp\setup.ps1 | **TBD** |
| **TBD** | src\WebApp\web.config | **TBD** |
| Generate  | src\WebApp\App_Data\jobs\continuous\Simulator\simulator.py | **TBD** |
| Generate  | src\WebApp\App_Data\jobs\continuous\DataSync\run.cmd | **TBD** |
| Generate  | src\WebApp\App_Data\jobs\continuous\DataSync\settings.job | **TBD** |
| Generate  | src\WebApp\App_Data\jobs\continuous\DataSync\sync.py | **TBD** |
| **TBD** | src\WebApp\flask\README.md | **TBD**
| **TBD** | src\WebApp\flask\app.py | **TBD** |
| Operationalize | src\WebApp\flask\model_management.py | **TBD** |
| Operationalize | src\WebApp\flask\aztk_cluster.py | **TBD** |
| **TBD** | src\WebApp\flask\spark\customScripts\jupyter.sh | **TBD** |
| **TBD** | src\WebApp\flask\spark\spark\.config\core-site.xml | **TBD** |
| **TBD** | src\WebApp\flask\spark\spark\.config\spark-defaults.xml | **TBD** |
| **TBD** | src\WebApp\flask\spark\spark\.config\spark-env.sh | **TBD** |
| **TBD** | src\WebApp\flask\static\* | Decorative .png files used in Notebooks |
| Dashboard | src\WebApp\flask\templates\*.html | HTML for Dashboard UX |
| Documentation | README.md | Home Page |
| Documentation | LICENSE | Text for Creative Commons License |
| Documentation | LICENSE_CODE | Text for MIT License |
| Documentation | docs\Architecture.md | Solution Template Architecture description - this file |
| Documentation | docs\Deployment.md | Step by step deployment walkthrough |
| Documentation | docs\Model-Train-and-Test.md | Train and Test descriptions for each use case |
| Documentation | docs\Model-operationalize | Operationalization description by use case |
| Documentation | docs\Developers-Guide.md | Guidelines to adapt the template for new scenarios |
| Documentation | docs\FAQ.md | Frequently asked questions about the architecture |
| Documentation | docs\Release-Notes.md | Notes on updates, known bugs and mitigations |
| Documentation | docs\AZTK-instructions.md | **TBD** |
| Documentation | docs\img\* | Image files for documentation |
| Documentation | docs\media\cortana-analytics-playbook-predictive-maintenance\* | **TEMPORARY - images for local copy of Azure AI Guide for Predictive Maintenance** |
| Documentation | docs\cortana-analytics-playbook-predictive-maintenance.md | **TEMPORARY - Local copy of Azure AI Guide for Predictive Maintenance. This will be removed once the main document is reviewed and submitted into Microsoft Docs** |
