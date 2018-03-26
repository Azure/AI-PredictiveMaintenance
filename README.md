# [Predictive Maintenance (PdM) Solution Template](https://gallery.cortanaintelligence.com/Solution/Enterprise-Reporting-and-BI-Technical-Reference-Implementation-2)

[![Deploy to Azure](https://raw.githubusercontent.com/Azure/Azure-CortanaIntelligence-SolutionAuthoringWorkspace/master/docs/images/DeployToAzure.PNG)](https://start.cortanaintelligence.com/track/Deployments/new/enterprisebiandreporting?source=GitHub)

<a href="https://start.cortanaintelligence.com/track/Deployments?type=enterprisebiandreporting" target="_blank">View deployed solution &gt;</a>

## Summary
This solution template provides a proof-of-concept (POC) implementation for a Predictive Maintenance scenario - namely, _predicting failure of sensor-monitored devices_. You can deploy this template into your Azure subscription in short time to demo or view its operation based on data generated in the template.

Documentation provided with the template explains the scenario, the data science behind the scenario, and the end to end architecture. In addition, the documentation discusses the common business problems in this space, the prerequisite data required to solve these problems, the data science behind solving these problems, how to adapt the template for other PdM scenarios, and how to scale the template for larger workloads.

## Audience

If you are a business decision maker (BDM) looking for ways to reduce the downtime and improve utilization of your critical equipment, see the section [Business Case](#Business-case).

If you are a technical decision maker (TDM) evaluating PdM technologies, review the section [Data Science for PdM](#Data-Science-for-PdM) in addition to the business case, to understand the requirements and processing for predictive analytics is different than query-based analytics.

If you are a sofware architect or developer, see the section [Architecture](#Architecture) in addition to the above.

## Quick Start

**Note:** If you have already deployed this solution, click [here](https://start.cortanaintelligence.com/Deployments) to view your deployment.

### Prerequisites
You need an Azure subscription and [sufficient quota for the services](https://blogs.msdn.microsoft.com/skeeler/2017/01/subscription-usage-and-quotas-in-the-azure-portal/)  listed in the section [Resource Consumption](#Resource-Consumption).

### What does this solution template offer
From a software design perspective, this template shows how to construct a complete PdM solution by surrounding an _inner machine learning loop_ with an _outer processing loop_, and the use of appropriate Azure services and products at each stage of the end to end processing pipeline. The adjoining documentation provides guidance on how to scale out this POC for production deployments.The inner machine learning loop for this solution template is based on  the  [_Advanced Predictive Maintenance Machine Learning Sample_]( https://github.com/Azure/MachineLearningSamples-PredictiveMaintenance/blob/master/Code/1_data_ingestion.ipynb).

From a problem solving perspective, this solution template shows how to _train_ a _classification_ model, based on a _training dataset_ from device sensor readings, maintenance and error logs, _test_ the model for its accuracy using a _test dataset_, and _score_ newly arriving device data using the model, and getting a _prediction_ on whether a device will fail in the next N days (N=7 in this example), and if yes, with the type of failure, along with the probability of failure.

The logical input, consisting of all _predictor variables_ would be several million rows like this.

| Timestamp | machine | pressure | speed | ... | model | age | ... | failure | error |
|-----------|---------|----------|-------|-----|-------|-----|-----|-----|-----|
|2016-01-01 12:00:00 | m27 | 162.37 | 445.71 | ... | model3 | 9 | ... | 0.0 | 0.3 |

This input would be sampled into a candidate data set of a few 10Ks of rows, split 40-30-30 between training, test, and validation data sets. Then the model would be trained 
and for each logical row of input, a row of scored output, like this:

| machine | ... _attributes_ ... | error | <span style="color:green">_will_fail_ | <span style="color:green">_failure_type_ | <span style="color:green">_probability_<span> |
|-----------|---------|-----|-------|-----------|--------------|
| m27 | ... | 0.3 | yes | F034 | 0.85034 |

NOTE: There are several solution templates titled Predictive Maintenance authored by Microsoft in GitHub and Microsoft sites. See section [Related Work](#Related-Work) for the list of these articles and their brief description, and about the need to consolidate them.

### Getting Started

**Estimated Provisioning Time:** 30 minutes **(TBD)**

You can have this solution template up and running in a few steps:

**Step 1:** Click on the Deploy button, shown above.

**Step 2:** Enter the details requested in the 'Create new deployment' form.

![Deploy_1](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/Deploy_1.png)

The deployment engine will create a resource group and start creating the Azure service instances and features that compose the deployment.

![Deploy_2](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/Deploy_2.png)

Upon successful completion of the deployment, you will be presented with a link to a web console/dashboard to operate the solution.

![Deploy_3](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/Deploy_3.png)

**Step 3:** Click on the link to the dashboard, and click Accept to the access request. This will provide you with the web console/dashboard. Click on **Analytics** in the left pane, which will bring up the UX to create the compute resources required to train the model.

![Deploy_4](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_4.png)

**Step 4:** Choose a SKU for the VM's (Standard_d2_v2), provide a username and password for the cluster, and start the training cluster creation.

![Deploy_5](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_5.png)

This will start the creation of a Spark cluster on Azure Batch via AZTK, which will take a few 10's of minutes to complete.

![Deploy_6](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_6.png)

**Step 5:** Upon completion of Spark cluster creation, you will have link to the Predictive Maintenance Dashboard. This is the main web console from which you will execute your main operations. The dashboard will show the cluster connection details.
![Deploy_7](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_7.png)

The next step is to connect to the Jupyter Notebooks that run the PySpark code for model training and testing. For this, you need to tunnel through to these Jupyter notebooks that are installed on the cluster itself. You can accomplish this in two ways:

If you have a SSH capable command line tool (CMD or other alternative), then you can directly cut paste the SSH command that shows up in the dashboard.

![Deploy_6a](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_6a.png)

Alternatively, you can download PuTTy from the link provided in the dashboard, and provide Port number: **8888** as input, and use the password that you established in **Step 4**.

![Putty_2](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/Putty_2.png)

**Step 6:** Then open a web browser and type http://localhost/8888. This will show the Jupyter dashboard with a folder for Notebooks.

![Deploy_8](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_8.png)

Open the Notebooks folder to see FOUR notebooks - one for each main task in the inner loop. Keep this tab open, you will return to this after each notebook run.

![Deploy_9](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_9.png)

**Step 7:** **Now, it is important that you open just one Notebook at a time.** Click on FeatureEngineering.ipynb - this opens up the notebook in a new tab, and starts up a _PySpark_ kernel in the cluster. 

![Deploy_10](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_10.png)

Click on section of the code and click on _Run_. This will complete the data preparation step of the inner machine learning loop. Once completed, **remember to shutdown the kernel from the Kernel pulldown tab, and close the browser tab**

**Step 8:** Go back to the list of notebooks. Confirm that FeatureEngineering.ipynb does not have the status of Running. Then click on ModelTraining.ipynb. Repeat the same steps as **Step 7**.

![Deploy_11](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_11.png)

**Step 9:** Go back to the list of notebooks. Confirm that ModelTraining.ipynb does not have the status of Running. Next to **test** the model, click on Operationalization.ipynb to test the model, and run it to completion.

![Deploy_12](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_12.png)

**Step 10:** As of this point, the model has been created and tested in the training cluster. The next step is to deploy this model for scoring - i.e. operationalizing the model for new data. This solution template supports online scoring - i.e. for each input record, the scoring engine returns a predicted value. This scoring engine is deployed as a web service in a Docker container which is then deployed on a Azure Kubernetes cluster.

For this, go back to the Predictive Maintenence dashboard (not the Jupyter dashboard) shown in **Step 5**. Click on Operationalization (also termed 'O16n') tab.

![Deploy_13](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_13.png)

There are five steps in the O16n tab:
- Register model with Azure ML.
- Register the Manifest.

![Deploy_14](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_14.png)

- Create Image to create a Docker Image for the web service. This will take some time, and when complete, it moves to the next step.

![Deploy_15](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_15.png)

- Create Service to create a web service in the docker image, and deploys the image to the cluster.

![Deploy_16](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_16.png)

Provide a service name here, and then click on Create. This quickly creates a service.

![Deploy_17](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_17.png)

- Finally click on the Consume link - this will generate the output in an Azure Table.

**Step 6** Next go look at the results in Azure.
- Install Azure Storage Explorer ([Install from here](https://azure.microsoft.com/en-us/features/storage-explorer/) if you do not have it).
- Connect to your Azure account, and from the portal, find your storage account from the resource group.

![Deploy_18](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/deploy_18.png)


 to tunnel to the Spark cluster via the VM.
or  you haeOnce the Spark cluster is deployed, 
- Follow the deployment instructions to authenticate, specify service, etc.
- This will deploy the solution with the components and process flow shown in the [Architecture](#Architecture) section, in a dedicated resource group.
- From the web console provided at the end of a successful deployment, run the featurization, model creation, and model scoring steps, based on instructions in the [User Guide](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/User%20Guides/README.md).
- To modify the solution to fit your scenario, follow the guidelines in the [Technical Guide](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Technical%20Guides/Technical%20Guide.md).
- Read the [Data Science Guide](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Data%20Science%20Guides/Data%20Science%20Guide.md) and the [Technical guide](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Technical%20Guides/Technical%20Guide.md) for details on the algorithms and services.
- Use the community forum at the bottom of this page for questions and clarifications.

### Resource Consumption

**Estimated Daily Cost:** $150.00 **(TBD)**

**TBD** - Provide the list of resources from the resource group.

## Business Case for PdM

Businesses require critical equipment and assets - from specialized equipment such as aircraft engines, turbines, and industrial chillers down to more familiar conveniences like elevators and xray machines - to be running at maximum utilization and efficiency.

Today, most businesses rely on _corrective maintenance_, where parts are replaced as they fail. This ensures parts are used completely (not wasting component life), but costs the business in both downtime and unscheduled maintenance (off hours, or inconvenient locations).

The next alternative is a _preventative maintenance_ - where the business heuristically estimates a safe lifespan of a component, and replaces it before failure. This avoids unscheduled failures, but still incurs the cost of scheduled downtime, under utilization of the component before its full life time, and the cost of labor.

The goal of _predictive maintenance_ is to optimize the balance between corrective and preventative maintenance, by enabling _just in time_ replacement of components only when they are close to failure. The savings come from both extending component lifespans (compared to preventive maintenance), and reducing unscheduled maintenance (over corrective maintenance), offering businesses a competitive ROI advantage over their peers with traditional maintenance procedures.

PdM solutions can help businesses that want to reduce  operational risk due to unexpected failures of equipment, require insight into the root cause of problems in an equipment as a whole, or from its subcomponents. Problems commonly observed in most businesses are:

| Typical Business Problems for PdM |
|---------------|
| Detect anomalies in equipment or system performance or functionality |
| Predict that an equipment may fail in the near future |
| Identify the remaining useful life of an equipment|
| Identify the predominant causes of failure of an equipment |
| Identify what maintenance actions need to be done when on an equipment |

The use case for this solution template is _predicting the failure of the equipment, and the _type of failure_, over the next N days_. For guidance on other business problems, and to learn about the benefits of applying PdM  techniques to these problems, see [Business perspective on PdM](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/User%20Guide/Business%20Guide.md).

<span style="color:gray">NOTE: Solution Templates for other PdM business problems</span>
- <span style="color:gray">For Public Preview, we will add the remaining useful lifetime scenario.</span>
- <span style="color:gray">For GA, we will add the remaining two scenarios.</span>

## Data Science for PdM

### Prerequisites
There are three prerequisites for a business problem to be solved by PdM  techniques:
- The problem has to be predictive in nature; that is, there should be a identifiable target or outcome to predict.
- The business should have a recorded history of past behavior of the equipment with both good and bad outcomes, along with the set of actions taken to mitigate bad outcomes.
- Finally, _sufficient_ enough data that is _relevant_ to the problem must be available. See [Data Preparation Guide](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Data%20Science%20Guides/Data%20Preparation.md) for details.

### Data requirements
The common _data elements_ for PdM problems can be summarized as follows:
- _Telemetry data:_ Output from sensors monitoring the operating conditions of the equipment - such as vibration, temperature, ambient temperature, magnetic field, humidity, pressure, sound, voltage, amperage, and so on.
- _Maintenance history:_ The repair history of a machine, including maintenance activities or component replacements, error code or runtime message logs. Examples are ATM machine transaction error logs, equipment maintenance logs showing the maintenance type and description, elevator repair logs, and so on.
- _Failure history:_ The failure history of a machine or component of interest, with the timestamp of the failures, types of failure, severity and so on. It is possible that failure history is contained within maintenance history, either as in the form of special error codes or order dates for spare parts. In those cases, failures can be extracted from the maintenance data. Examples are ATM cash withdrawal failure error logs, elevator door failures, turbine failure dates, and so on.
- _Equipment features_: The metadata specific to each individual equipment. Examples for a pump or engine are size, make, model, location, installation date; for a circuit breaker, technical specs like voltage and amperage levels.
- In addition, different business domains may have a variety of other data sources that influence failure patterns not listed here. These should be identified by consulting the domain experts when building predictive models.

The two main _data types_ observed in PdM are:
- _temporal/time series/historian data_: Failure history, machine conditions, repair history, usage history are time series indicated by the timestamp of data collection.
- _static metadata_: Machine and operator specific features, are static - they usually describe the technical specifications of machines or operator’s properties.

### Data Preparation

This is an exercise that is equal in importance to model creation for any AI problem, let alone predictive maintenance. Attributes for ML algorithms can be _numerical_ (continuous numbers), _categorical_ (discrete categories - either numbered or in text), _ordinal_ (categorical, but with values in order), _n-grams_ (a text phrase split into various combinations of _n_ words). In general, some of the key actions for data preparation are:

_Data selection_ - we have already discussed the kind of data we need to select for the predictive maintenance problem in the previous section.

_Data preprocessing_ - this step entails _formatting_ the data fields to have the right representation and precision; _cleaning_ the data that is incomplete, removing data that is irrelevant to the problem, or anonymizing sensitive data; _sampling_ down the data if it is very large.

_Data transformation_ or _Feature Engineering_ - in this step, data is transformed from its current state to a new state to fit the problem domain and the ML algorithm(s) that you plan to use. Three categories of transformations are common:
- _Scaling_: Many ML algorithms may require the attributes to be in a common scale between 0 and 1 - achieved by a process called _normalization_. _Binning_ is another scaling transformation - where a continuous range of numbers like age can be binned into 5 or 10 discrete age groups.
- _Decomposition_: A feature representing a complex concept could be split into its constituent parts, as in a timestamp being split into its day and time components - possibly because only the knowledge of the day matters for the problem at hand. Example transformations are _n-gram_ and _orthogonal sparse bigram_ for text.
- _Aggregation_: Many features aggregated into a single feature (reverse of decomposition) - an example is and _cartesian_ transformation of categorical attributes; or multiple instances of a feature occurrence aggregated into a single value - typically seen in time series and other voluminous and/or granular data. 

Data preparation for PdM will require strong domain expertise and data wrangling up-skilling:
- While industrial automation is a mature domain, the world of IoTs and open device data management is still in its infancy. There are no data standards or best practice hueristics for collecting, formatting and managing data. This makes data selection a custom activity. 
- Even within a specific industrial segment, say [industial chillers](https://www.achrnews.com/articles/106508-chiller-market-grows-diversifies), there are no formal standard set of attributes or informal hueristics on the the data preparation required for these attributes.

The good news is that [Azure ML's Data Wrangling](https://www.youtube.com/watch?v=9KG0Sc2B2KI) capability makes the mechanics of data preparation automated or semi-automated as possible. The data preparation steps for the _failure prediction problem_ described in this template is discussed in [Failure Prediction - Data Preparation](#Failure-Prediction-Data-Preparation).

**NOTE**: The content above was adapted from [here](https://docs.aws.amazon.com/machine-learning/latest/dg/data-transformations-reference.html) and [here](https://machinelearningmastery.com/how-to-prepare-data-for-machine-learning/) (**TBD** - We need equivalent Microsoft documentation in the introduction to Azure ML Data Wrangling, even if this content is repetitive and available in textbooks).

### AI Techniques

The PdM business problems listed above can be mapped to specific AI techniques and a corresponding algorithm for each AI technique - as tabulated below.

|#|PdM Business Problem | AI Technique | Algorithm choices |
|-|---------------|--------------|-------------------|
|1| Detecting operational anomalies | AI Technique TBD | Algorithm TBD |
|2| Predicting the Failure | Multi-class classification | Random Forest, Decision Trees |
|3| Remaining useful life | Deep Neural Networks | Long Short Term Memory (LSTM) |
|4| Predominant Causes of failure | AI Technique TBD | Algorithm TBD |
|5| Maintenance actions to be done | AI Technique TBD | Algorithm TBD |

The AI technique and algorithm for the _failure prediction problem_ described in this template is discussed in [Failure Prediction - Algorithm](#Failure-Prediction-Algorithm). For a general discussion on AI Techniques and algorithms for PdM, see the [Data Science Guide for PdM](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Data%20Science%20Guides/Data%20Science%20Guide.md).

## Architecture
Predictive Maintenance solution deployments are required in three fronts:
- _On Prem_ - for scenarios where customers do not want to connect to the cloud, or have devices that cannot be connected to the Internet, but with the data delivered via local, private networks to central, on-prem servers. This the most prevalent scenario today, based on the previous generation of factory automation is done this way.
- _Cloud based_ - centralized ML and analytics in the cloud to process delivered via the Internet from IoTs, with devices are managed from the cloud via a centralized command and control. This is the future.
- _Edge based_ - for scenarios where the modeling is done centrally in the cloud, but the models have to be delivered to edge devices that cannot be connected to the cloud.

The Cloud Based architecture is described in this solution template.

![PdM_Solution_Template](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/PdM_Solution_Template.png)

### Operational walk-through

#### INGEST

This solution template provides a general purpose [Sensor Data Simulator](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/src/WebApp/App_Data/jobs/continuous/Simulator/simulator.py) along with [documentation](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/src/Notebooks/DataGeneration.ipynb) to produce synthesized data for specific measurements of an equipment such as temperature, pressure etc. 

Multiple streams of sensor data are ingested into an [Azure IoT Hub](https://azure.microsoft.com/en-us/services/iot-hub/)

#### STAGE

#### PROCESS

#### TRAIN

#### SCORE

#### PUBLISH

#### CONSUME


# Predicting the Failure of a device

## Problem Statement
The problem here is to predict the failure of a device, indicating the type of failure, along with the probability (chance) of its occurrence, over the next N days, given a set of _predictor variables_ such as temperature, pressure, etc over time.

Stated in modeling terms, this is a _multi-class classification_ problem that _classifies_ the target variable _failure_ to one of the different failure types, called _classes_. From the [recommended set of algorithms](https://docs.microsoft.com/en-us/azure/machine-learning/studio/algorithm-cheat-sheet), we choose the one that affords accuracy and speed of model creation, namely, _multi-class decision forest_.

## Data Preparation

## Model Creation

### Failure Prediction - Model Testing

### Failure Prediction - Model Validation

## Architectural/Solution Perspective

 Solutions for predictive maintenance are required in two areas:
- Cloud based - for centralized processing, analytics and ML based on data delivered via the Internet from devices.
- Edge based - for scenarios where the devices are not, or cannot be, connected to the Internet, requiring the analytics and its results to happen right at the edge.

### How it works - in a nutshell


### TODO: add info and links

[Train](https://quickstart.azure.ai/Deployments/new/training)

[Operationalize](https://quickstart.azure.ai/Deployments/new/operationalization)
