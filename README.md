# Predictive Maintenance (PdM) Solution Template


## Summary
This solution template provides an end to end, proof-of-concept implementation for a Predictive Maintenance scenario - namely, failure prediction of sensor-monitored industrial equipment. You can easily deploy this template into an Azure subscription to demo or view its operation based on preconfigured sample data in the template. Documentation provided with the template explain the scenario, the data science behind the scenario, and the end to end architecture used in the template.

Besides being a point solution to a specific PdM scenario, the template also packages in-depth documentation explaining the common business problems in this space, the prerequisite data required to solve these problems, the data science behind solving these problems, how to adapt the template for other PdM scenarios, and how to scale the template for larger workloads.

## Audience
This template caters to a wide audience.
- If you are a business decision maker (BDM) looking for ways to reduce the downtime and improve utilization of your critical assets, see [Business perspective on PdM](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/User%20Guide/Business%20Guide.md).
- If you are a technical decision maker (TDM) or a consultant evaluating PdM technologies, and/or want to make a pitch to BDM on the use of PdM technologies, read the business perspective, and additionally [Data Science Guide for PdM](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Data%20Science%20Guides/Data%20Science%20Guide.md). This will help you understand how AI data and modeling requirements, processing, and result semantics are different than typical query-based analytics from a data store or stream analytics of data in motion.
- If you are an architect or developer with the specific need to implement this solution, read the data science perspective and the [Technical Guide for PdM](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Technical%20Guides/Technical%20Guide.md) for more detailed content on data management and AI techniques.
 

## Description

**Note:** If you have already deployed this solution, click [here](https://start.cortanaintelligence.com/Deployments) to view your deployment.

**Estimated Daily Cost:** $150.00 **(TBD)**

**Estimated Provisioning Time:** 30 minutes **(TBD)**

Businesses require critical equipment and assets - from highly specialized equipment like aircraft engines, turbines, and industrial chillers down to more familiar conveniences like elevators and xray machines - to be running at maximum utilization and efficiency. While it is obvious that unscheduled downtime of such equipment can be extremely expensive, scheduled maintenance of the equipment could also be expensive in terms of high cost of specialized labor and downtime. The ideal solution is to be able to _predict_ the possibility of a failure in the near future, based on historical patterns of equipment behavior from sensor-based data, maintenance records and other error reports, and then perform just in time maintenance of the equipment. Such _predictive maintenance_ offers businesses a competitive advantage in terms of improving utilization and ROI compared to their peers with traditional maintenance procedures.

## Business Case 

PdM solutions can help businesses that want to reduce  operational risk due to unexpected failures of equipment, require insight into the root cause of problems in an equipment as a whole, or from its subcomponents. The problems that are commonly observed in most businesses are:

| Typical Business Problems for PdM |
|---------------|
| Predict that an equipment may fail in the near future |
| What is the remaining useful life of an equipment |
| Identify the predominant causes of failure of an equipment |
| Identify what maintenance actions need to be done on an equipment |

The use case for this solution template is the first business problem - namely **predicting the failure of the equipment, and the _type of failure_, over the next N days**.

**Note: Solution Templates for other PdM business problems**
- For Public Preview, we will add remaining useful lifetime.
- For GA, we will update the solution template with examples for all the business problems listed above.**

For guidance on other business problems, and to learn about the benefits of applying PdM  techniques to these problems, see [Business perspective on PdM](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/User%20Guide/Business%20Guide.md).

## Data Science for PdM

### Prerequisites
There are three prerequisites for a business problem to be solved by PdM  techniques:
- The problem itself has to be predictive in nature
- The business should have a recorded history of past behavior of the equipment with both good and bad outcomes, along with the set of actions taken to mitigate bad outcomes.
- Finally, _sufficient_ enough data that is _relevant_ to the problem must be available. This is described in more detail in the [Data Preparation Guide](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Data%20Science%20Guides/Data%20Preparation.md). 

### Data requirements
The common **data elements** for PdM problems can be summarized as follows:
- _Equipment features_: The features specific to each individual equipment. Examples for a pump or engine are size, make, model, location, installation date; for a circuit breaker, technical specs like voltage and amperage levels, 
- _Telemetry data:_ Output from sensors monitoring operation conditions of the equipment - such as vibration, object temperature, ambient temperature, magnetic field, humidity, pressure, sound, voltage or amperage levels, and so on.
- _Maintenance history:_ The repair history of a machine, including maintenance activities or component replacements, error code or runtime message logs. Examples are ATM machine transaction error logs, equipment maintenance logs showing the maintenance type and description, elevator repair logs, and so on.
- _Failure history:_ The failure history of a machine or component of interest.
It is possible that failure history is contained within maintenance history, either as in the form of special error codes or order dates for spare parts. In those cases, failures can be extracted from the maintenance data. Examples are ATM cash withdrawal failure error logs, elevator door failures, turbine failure dates, and so on.
- In addition, different business domains may have a variety of other data sources that influence failure patterns not listed here. These should be identified by consulting the domain experts when building predictive models.

The two main **data types** observed in PdM are _temporal/time series/historian data_ and _static data_. Failure history, machine conditions, repair history, usage history are time series indicated by the timestamp of data collection. Machine and operator specific features, are more static, since they usually describe the technical specifications of machines or operator’s properties.

### Data Preparation

This solution template offers a general purpose [Sensor Data Simulator](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/src/Notebooks/DataGeneration.ipynb) to produce synthesized data for various measurements of an equipment such as temperature, pressure etc. Over time, this will be combined into the [Azure IoT Device Simulator](https://docs.microsoft.com/en-us/azure/iot-suite/iot-suite-device-simulation-explore).

A separate [data generator](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/src/WebApp/App_Data/jobs/continuous/Simulator/simulator.py) combines these individual sensor data along with the other data elements mentioned above to provide the schematized data. This data will be provided as  input for model training, testing and new data to be scored by the model.

Once a relevant and sufficient data stream has been composed, the next step is to prepare the data for the specific problem being solved. This may entail formatting, cleaning, and transforming the data (called _featurization_) to make it suitable for the chosen algorithm - a process collectively called **data wrangling**. The data preparation steps for the _failure prediction problem_ described in this template is discussed in [Failure Prediction - Data Preparation](#Failure-Prediction-Data-Preparation). 

### AI Technique

The PdM business problems listed above can be mapped to specific AI techniques and a corresponding algorithm for each AI technique - as tabulated below.

|#|PdM Business Problem | AI Technique | Algorithm choices |
|-|---------------|--------------|-------------------|
|1| Predicting the Failure of an equipment | Multi-class classification | Random Forest, Decision Trees |
|2| Remaining useful life of an equipment | Deep Neural Networks | Long Short Term Memory (LSTM) |
|3| Predominant Causes of failure of an equipment | AI Technique TBD | Algorithm TBD |
|4| Maintenance actions to be done on an equipment | AI Technique TBD | Algorithm TBD |

The AI technique and algorithm for the _failure prediction problem_ described in this template is discussed in [Failure Prediction - Algorithm](#Failure-Prediction-Algorithm). For a general discussion on AI Techniques and algorithms for PdM, see the [Data Science Guide for PdM](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Data%20Science%20Guides/Data%20Science%20Guide.md).

## Predicting the Failure of a device

### Problem Statement translated to AI Technique and Algorithm
The problem here is to predict the failure of a device, indicating the type of failure, along with the probability (chance) of its occurrence, over the next N days, given a set of _predictor variables_ such as temperature, pressure, etc over time.

Stated in modeling terms, the problem here is to _classify_ the target variable _failure_ to one of the different failure types, called _classes_. More accurately, this is a _multi-class classification_ problem. From the [recommended set of algorithms](https://docs.microsoft.com/en-us/azure/machine-learning/studio/algorithm-cheat-sheet), the one that affords accuracy and can quickly create a model - namely, _multi-class decision forest_.

### Failure Prediction - Data Preparation

### Failure Prediction - Model Creation

### Failure Prediction - Model Testing

### Failure Prediction - Model Validation

## Architectural/Solution Perspective

 Solutions for predictive maintenance are required in two areas:
- Cloud based - for centralized processing, analytics and ML based on data delivered via the Internet from devices.
- Edge based - for scenarios where the devices are not, or cannot be, connected to the Internet, requiring the analytics and its results to happen right at the edge.

![Architecture](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/README-Generic-Architecture.png)

### How it works - in a nutshell

### INGEST

### STAGE

### PROCESS

### TRAIN

### SCORE

### PUBLISH

### CONSUME

### TODO: add info and links

[Train](https://quickstart.azure.ai/Deployments/new/training)

[Operationalize](https://quickstart.azure.ai/Deployments/new/operationalization)
