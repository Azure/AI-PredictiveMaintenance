# Predictive Maintenance (PdM)


# Summary
This solution template provides an end to end, proof-of-concept implementation for a Predictive Maintenance scenario - namely, failure prediction of sensor-monitored industrial equipment. Documentation provided with the template explain the data science and architecture used in the template. Further, in-depth design guidelines explain how to adapt the template for other predictive maintenance scenarios, and how to scale the template for larger workloads.

# Description

**Note:** If you have already deployed this solution, click [here](https://start.cortanaintelligence.com/Deployments) to view your deployment.

**Estimated Daily Cost:** $150.00 **(TBD)**

**Estimated Provisioning Time:** 30 minutes **(TBD)**

Businesses require critical equipment and assets - from specialized ones like aircraft engines, turbines, and industrial chillers down to everyday conveniences like elevators and xray machines - to be running at maximum utilization and efficiency. While it is obvious that unscheduled downtime of such equipment can be extremely expensive, scheduled maintenance of the equipment could also be expensive in terms of high cost of specialized labor and downtime. The ideal solution is to be able to _predict_ the possibility of a failure in the near future, based on historical patterns of equipment behavior from sensor-based data, maintenance records and other error reports, and then perform just in time maintenance of the equipment. Such _predictive maintenance_ offers businesses a competitive advantage in terms of improving utilization and ROI compared to their peers with traditional maintenance procedures.

The rest of the content for this solution template is organized as follows:
- [Business perspective](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/User%20Guides/Business%20Guide.md)
- [Data Science Guide](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Data%20Science%20Guides/Data%20Science%20Guide.md)
- [Architecture](#Architecture)
- [Technical Guide](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Technical%20Guides/Technical%20Guide.md)

# Business Perspective

**BEGIN - Section copied verbatim from the [Playbook](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/cortana-analytics-playbook-predictive-maintenance)**

The impact of unscheduled equipment downtime can be extremely destructive for businesses. It is critical to keep field equipment running in order to maximize utilization and performance and by minimizing costly, unscheduled downtime. Simply, waiting for the failure to occur is not affordable in today’s business operations scene. To remain competitive, companies look for new ways to maximize asset performance by making use of the data collected from various channels. One important way to analyze such information is to utilize predictive analytic techniques that use historical patterns to predict future outcomes. One of the most popular of these solutions is called Predictive Maintenance which can generally be defined as but not limited to predicting possibility of failure of an asset in the near future so that the assets can be monitored to proactively identify failures and take action before the failures occur. These solutions detect failure patterns to determine assets that are at the greatest risk of failure. This early identification of issues helps deploy limited maintenance resources in a more cost-effective way and enhance quality and supply chain processes.

With the rise of the Internet of Things (IoT) applications, predictive maintenance has been gaining increasing attention in the industry as the data collection and processing technologies has matured enough to generate, transmit, store and analyze all kinds of data in batches or in real-time. Such technologies enable easy development and deployment of end-to-end solutions with advanced analytics solutions, with predictive maintenance solutions providing arguably the largest benefit.

Business problems in the predictive maintenance domain range from high operational risk due to unexpected failures and limited insight into the root cause of problems in complex business environments. The majority of these problems can be categorized to fall under the business questions tabulated below.


|#|Common Problem |
|-|---------------|--------------|
|1| Probability that an equipment fails in the near future |
|2| Remaining useful life of an equipment |
|3| Predominant Causes of failure of an equipment |
|4| Maintenance actions to be done on an equipment |


By utilizing predictive maintenance to answer these questions, businesses can:
- Reduce operational risk and increase rate of return on assets by identifying failures before they occur.
- Reduce unnecessary time-based maintenance operations and control cost of maintenance
- Lower inventory costs by reducing inventory levels by predicting the reorder point
- Discover patterns connected to various maintenance problems
- Improve overall brand image, eliminate bad publicity and resulting lost sales from customer attrition.
- Get key performance indicators such as health scores to monitor real-time asset condition
- Plan capital allocation based on estimates of the remaining lifespan of assets
- Get recommendation for proactive maintenance activities and estimated order dates for replacement of parts

**END - Section copied verbatim from the [Playbook](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/cortana-analytics-playbook-predictive-maintenance)**

# Data Science Perspective

For a business problem to be solved by predictive maintenance techniques, the problem itself has to be predictive in nature, a clear path of action should exist in order to prevent failures when they are detected beforehand, and most importantly, data with sufficient quality to support the use case should be available.

## Data Requirements

First, let us focus on the data requirements to build a successful predictive maintenance solution.

**Data Relevancy** A predictive model is "trained" to recognize hidden patterns from historical data on the equipment. Typically, this data has descriptive features or attributes of a piece of equipment, and a specific "target" behavior of the equipment for those specific set of features. In the simplest case, the training data is a sufficient set of examples where the target value is a  true or false - indicating whether an equipment failed under specific conditions of temperature, pressure, vibration, torque, and more such attributes that impact the equipment's behavior. A model trained with such examples is then expected to "predict" the target value when provided just the features of new examples. To make accurate predictions, it is important for the model to accurately capture the relationship between features and the target of prediction. So a key prerequisite is to have *representative* training data, which have features that actually have predictive power towards the target of prediction; meaning the data should be relevant to the prediction goal to expect accurate predictions. Examples:

- If the target is to predict failures of turbines, the training attributes should contain telemetry reflecting the status of the turbine blades and the rotor and other components that make up the turbine under varying conditions of inputs.
- If the target is to predict failure of an electronic components, measurements of voltage, current, resistance, capacitance besides heat, dust level, and other factors need to be recorded in terms of the relevance to the actual failure.

The data also needs to be directly related to the operating conditions of the target being predicted, at the appropriate granularity. In the turbine example, the target of failure prediction could be the entire turbine, or a specific component of the turbine, such as the blade, the shaft, the yaw drive, gear or the motor; or even their subcomponents.  of these individual components. It would be incorrect to build a failure model for the more general component without the data from all sub-components; conversely, predicting the failure of a subcomponent based on higher level data would also be inaccurate. In general, it is more sensible to predict specific failure events than more general ones.

To build predictive models, the user should understand the data relevancy requirements and provide the domain knowledge required select relevant subsets of data for analysis. Three essential data sources are required to build accurate models for predictive maintenance solutions:

- *Failure History:* When building predictive models that predict failures, the ML algorithm needs to learn the normal operation pattern as well as the failure pattern through the training process. It is essential for the training data to contain sufficient number of examples in both categories in order to learn these two different patterns. Failure events can be found in maintenance records and parts replacement history or anomalies in the training data can also be used as failures as identified by the domain experts. But in typical scenarios, failure events are rare. There are however [some advanced techniques](https://blogs.technet.microsoft.com/machinelearning/2016/04/19/evaluating-failure-prediction-models-for-predictive-maintenance/) to handle this data imbalance.
- *Maintenance/Repair History:* An essential source of data for predictive maintenance solutions is the detailed maintenance history of the asset containing information about the components replaced, preventive maintenance activates performed, etc. It is extremely important to capture these events as they record the degradation patterns.
- *Machine Conditions:* In order to predict how many more days (hours, miles, transactions, etc.) a machine lasts before it fails, we assume the machine’s health status degrades over time during its operation. Therefore, we expect the data to contain time-varying features that capture this ageing pattern and any anomalies that lead to degradation. In IoT applications, the telemetry data from different sensors represent one good example. In order to predict if a machine is going to fail within a time frame, ideally the data should capture degrading trend during this time frame before the actual failure event.

**Data Sufficiency** A typical question is how many failure events are required to train a model, and how many is considered as "enough"? The answer to this question is still "it depends" - but there are well known heuristics and iterative methodologies to determine data sufficiency - please refer the discussions [here](https://machinelearningmastery.com/much-training-data-required-machine-learning/).

https://datascience.stackexchange.com/questions/19980/how-much-data-are-sufficient-to-train-my-machine-learning-model

**END**

## PdM problems mapped to AI Techniques

In this section, we map each of the PdM scenarios listed above to a corresponding data science problem, and then map each problem to a possible set of machine learning techniques that can be used to solve the problem. Each technique may have its own unique data and data preparation requirements.

The common predictive maintenance problems mapped to AI techniques is tabulate below.

|#|Common Problem | AI Technique | Algorithm choices |
|-|---------------|--------------|-------------------|
|1| Probability that an equipment fails in the near future | AI 01 | Algo 01 |
|2| Remaining useful life of an equipment | AI 02 | Algo 02 |
|3| Predominant Causes of failure of an equipment | AI 03 | Algo 03 |
|4| Maintenance actions to be done on an equipment | AI 04 | Algo 04 |

## Failure Probability of an equipment

Talk about the different kinds of data that is gathered for predictive maintenance.

[**Andrew's Notebook on Data Generation**](https://github.com/wdecay/PredictiveMaintenance-Simulation/blob/master/sound.ipynb)

### Algorithm
Describe the algorithm we are planning to use

### Data (Preparation) Requirements
This dataset will be used in the generic POC implementations to demo the first of the predictive maintenance scenarios - viz. Failure probability of the equipment. 

## Remaining Useful Life of an equipment

### Algorithm

### Data (Preparation) Requirements

## Causes of Failure of Equipment

### Algorithm

### Data (Preparation) Requirements

## Maintenance Actions to be performed on an equipment

### Algorithm

### Data (Preparation) Requirements

# Architectural/Solution Perspective

 Solutions for predictive maintenance are required in two areas:
- Cloud based - for centralized processing, analytics and machine learning based on data delivered via the Internet from IoT devices
- Edge based - for scenarios where the devices are not, or cannot be, connected to the Internet, requiring the analytics and its results to happen right at the edge.

## Failure Prediction (generic template)

![Architecture](./img/README-Generic-Architecture.png)


### How it works - in a nutshell
**TO BE DONE - ANDREW/RAM/NAVEEN - FINALIZE AND UPDATE THIS BY 02/20**
1. The simulation data is streamed by a newly deployed Azure Web Job, AeroDataGenerator.
2. This synthetic data feeds into the Azure Event Hubs service as data points.
3. Two Azure Stream Analytics jobs analyze the data to provide near real-time analytics on the input stream from the event hub. One of the Stream Analytics jobs archives all raw incoming events to the Azure Storage service for later processing by the Azure Data Factory service, and the other publishes results onto a Power BI dashboard. 
4. The HDInsight service is used to run Hive scripts (orchestrated by Azure Data Factory) to provide aggregations on the raw events that were archived by the aforementioned Stream Analytics job.
5. The Azure Machine Learning service is used (orchestrated by Azure Data Factory) to make predictions on the remaining useful life (RUL) of particular aircraft engine given the inputs received.
6. Azure SQL Database is used (managed by Azure Data Factory) to store the prediction results received from the Azure Machine Learning service. These results are then consumed in the Power BI dashboard. A stored procedure is deployed in the SQL Database and later invoked in Azure Data Factory pipeline to store the ML prediction results into the scoring result table.
7. Azure Data Factory handles orchestration, scheduling, and monitoring of the batch processing pipeline. 
8. Finally, Power BI is used for results visualization, so that aircraft technicians can monitor the sensor data from an airplane or across the fleet in real time and use visualizations to schedule engine maintenance.

### INGEST

### STAGE

### PROCESS

### TRAIN

### SCORE

### PUBLISH

### CONSUME

## Remaining Useful Life of components

![Architecture](./img/README-Generic-Architecture.png)

### Key changes to the design

### INGEST

### STAGE

### PROCESS

### TRAIN

### SCORE

### PUBLISH

### CONSUME

## Remaining Useful Life of components

![Architecture](./img/README-Generic-Architecture.png)

### Key changes to the design

### INGEST

### STAGE

### PROCESS

### TRAIN

### SCORE

### PUBLISH

### CONSUME

## Causes of Failure

![Architecture](./img/README-Generic-Architecture.png)

### Key changes to the design

### INGEST

### STAGE

### PROCESS

### TRAIN

### SCORE

### PUBLISH

### CONSUME

# TODO: add info and links

[Train](https://quickstart.azure.ai/Deployments/new/training)

[Operationalize](https://quickstart.azure.ai/Deployments/new/operationalization)
