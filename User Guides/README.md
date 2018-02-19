# Predictive Maintenance (PdM)

**[ED - ramkri - Goal statement]** *To promote Microsoft AI adoption by our customers, we have implemented 37 solution templates and tutorials. The solution templates - with a few exceptions - are not end to end complete; they demo one aspect of machine learning with simulated data, with limited explanation on the why and what of the process. None of these solution templates can be verified to have taken a customer from proof-of-concept to production.*

*We have generated voluminous online content from various AI related organizations across Microsoft. Most of the content, with a few exceptions like [this playbook](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/cortana-analytics-playbook-predictive-maintenance), introduce the business problem, and skip straight to pitching Azure technology, without explaining the data science behind solving the business problem, and why specific technology is needed in the first place. We stamp these recommendations wtih the Microsoft brand - calling them "reference architectures", when these are mostly Visio drawings put up by creative architects or PMs with no live, tested, implementations to back them up. Others, like [this one](https://blogs.microsoft.com/iot/2017/02/28/future-focused-stop-thinking-in-the-past-and-get-ahead-of-the-unexpected-with-iot-2/) address the BDM (business decision maker) concerns well, but do not back that with a technology demo or POC that she can hand off to her technical team for evaluation. To confuse the user further, our AI Gallery has thousands of online submissions from random users, wiz thout any vetting for their quality or capabilities. So if a user searches for "Predictive Maintenance using Azure", she gets 1076 hits from the AI Gallery - and then has to  through a filtering exercise to isolate items of good quality. So while we  may have thousands of hits at the AI Gallery, we do not have one veriable NOT ONE VERIxxxxxxxxFIABLE PRODUCTION IMPLEMENTATION that can be attributed to an asset from this gallery. This disconnect limits our Field's ability to ramp up quickly on Azure AI, earn the trust of their customers, and influence and onboard customers to the Azure platform. Needless to say, this disconnect is equally frustrating for ISVs, Partners, and customers to put together solutions quickly.*

*This README is part of an AI Solution Template Revamp effort to take the user and/or Field personnel through a disciplined process of mapping the business problem to AI, from the AI problem to the AI technique(s), and then showcasing the relevant Azure ML technology for the inner ML loop, and Azure Data/Storage/Compute/Network  services for the outer data and processing loops. Once we establish this, the goal is to show users how to plug and play with technology choices in each stage of the end to end solution. For the data science components, we will provide 300 and 400 level content on the alternative techniques and/or alternative algorithms for the technique, with their corresponding data and preparation requirements. For the architectural components, we will provide design guideline documentation on scaling each stage from proof-of-concept to production. Given this frame, we can refactor the current 26+9 Microsoft-authored solution templates down to a manageable set of 10-12 templates, around which we can build a community of MVPs (most value participants) as stewards of the content in an open source model. In parallel, we can triage the gallery and remove a large number of the stale, partial, incorrect submissions, and roll up the good ideas into these candidate templates. This way, a well-informed Field can sell Azure AI more efficiently, and Engineering can move on to the challenges of showcasing enterprise-grade reference implementations to accelerate production wins. The improved solution templates and content will directly benefit users looking to build Azure AI solutions.*

*We start this effort in Scandium with Predictive Maintenance, and rinse and repeat this model for more business problems in Manufacturing, Retail, Finance, and Health*

-------------------------------------------------------------------------------------------------
# Summary

This solution template provides proof-of-concept implementations of 1-click deploy PdM solutions along with analytical and architectural guidelines to adapt them for different customer scenarios in this space. The template provides an end to end implementation for a candidate scenario - say failure prediction. The guidelines and tutorials explain how to adapt this generic implementation to solve common predictive maintenance scenarios in business problems across different industries. The documentation provides the business perspective for predictive maintenance, and the Data Science perspective on mapping the business problem(s) to AI, and the Architect's perspective on putting an end to end solution. The guidelines explain the solution development process in terms of Microsoft best practices, called Team Data Science Process (TDSP), with references to in-depth content and training materials. Design guidelines to scale the infrastructure for a production implementation with continuous integration continuous development (CICD) is also provided.

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