---
title: Azure AI Playbook for Predictive Maintenance (PdM) Solutions | Microsoft Docs
description: A comprehensive description of the data science that powers predictive maintenance solutions in multiple vertical industries.
services: cortana-analytics
documentationcenter: ''
author: fboylu
manager: jhubbard
editor: cgronlun

ms.assetid: 2e8b66db-91eb-432b-b305-6abccca25620
ms.service: cortana-analytics
ms.workload: data-services
ms.tgt_pltfrm: na
ms.devlang: na
ms.topic: article
ms.date: 03/14/2017
ms.author: fboylu

---
# Azure AI Playbook for Predictive Maintenance (PdM) Solutions
_Contributors: [Fidan Boylu Uz, PhD](https://github.com/fboylu), [Gary Ericson](https://github.com/garyericson); [Ramkumar Krishnan](https://github.com/ramkumarkrishnan)_

## Summary

Predictive maintenance is a popular application of predictive analytics that can help businesses in several industries achieve high asset utilization and savings in operational costs. This playbook introduces several industry-specific business scenarios for PdM. The playbook explains the process of qualifying these business scenarios for PdM, along with the data requirements and modeling techniques to build PdM solutions. It describes the data science process behind building these models - such as feature engineering, model creation, and model operationalization. To complement the key concepts, this playbook provides pointers to solution templates and reference architectures that can help you quickly build these PdM solutions on Azure. In essence, this playbook brings together the business and analytical guidelines and best practices that can help you successfully develop and deploy PdM solutions using the [Microsoft Azure AI platform](https://azure.microsoft.com/en-us/overview/ai-platform) technology.

### Playbook overview and target audience
The first half of this playbook will benefit business decision makers (BDMs). It describes typical business problems, the benefits of implementing PdM to address these problems, and list some common use cases. In the second half, the data science behind PdM is explained, and pointers to several PdM solution implementations are provided. Technical decision makers (TDMs) will find this content useful. 

| Start with ... | If you are ... |
|:---------------|:---------------|
| [Business case for PdM](#Business-Case-for-PdM) |a business decision maker (BDM) looking to reduce downtime and operational costs, and improving utilization of  equipment | 
| [Data Science for PdM](#Data-Science-for-PdM) |a technical decision maker (TDM) evaluating PdM technologies to understand the unique data processing and AI requirements for predictive maintenance |
| [Solution Templates for PdM](#Solution-Templates-for-PdM)|a software architect or AI Developer looking to quickly stand up a demo or proof-of-concept | 

### Prerequisite knowledge
The BDM content does not expect the reader to have prior data science knowledge. For the TDM content, basic knowledge of statistics and data science is helpful. Knowledge of Azure Data and AI services, Python, R, PowerShell, XML, and JSON helps. Solution templates are implemented in _.Net_, with a few examples in _Node.js_, and _Java_. The Appendix provides several pointers to training and documentation to help you develop these skills.

## **Business Case for Predictive Maintenance**

This section is organized as follows:

- [Business Problems in PdM](#Business-Problems-in-PdM)
- [Qualifying problems for PdM](#Qualifying-problems-for-PdM)
- [Sample PdM Use cases](#Sample-PdM-Use-Cases)

Businesses require critical equipment to be running at peak efficiency and utilization to realize their return on capital investments. These assets could range from aircraft engines, turbines, elevators, and industrial chillers - that cost millions - down to everyday appliances like photocopiers, coffee machines, and water coolers.
- By default, most businesses rely on _corrective maintenance_, where parts are replaced as they fail. Corrective maintenance ensures parts are used completely (not wasting component life), but costs the business both in downtime and unscheduled maintenance requirements (off hours, or inconvenient locations).
- At the next level, businesses practice  _preventive maintenance_, where they determine the useful lifespan for a part, and maintain or replace it before a failure. Preventive maintenance avoids unscheduled and catastrophic failures. But the high costs of scheduled downtime, under-utilization of the component before its full lifetime of use, and labor still remain.
- The goal of _predictive maintenance_ is to optimize the balance between corrective and preventative maintenance, by enabling _just in time_ replacement of components. This approach only replaces those components when they are close to failure. By extending component lifespans (compared to preventive maintenance) and reducing unscheduled maintenance and labor costs (over corrective maintenance), businesses can gain cost savings and competitive advantages.

## Business Problems in PdM
Businesses face high operational risk due to unexpected failures and have limited insight into the root cause of problems in complex systems. Some of the key business questions are:

- Detect anomalies in equipment or system performance or functionality
- Predict that an asset may fail in the near future
- Estimate the remaining useful life of an asset
- Identify the main causes of failure of an asset
- Identify what maintenance actions need to be done, by when, on an asset

Typical goal statements from PdM are listed below.

- Reduce operational risk of mission critical equipment.
- Increase rate of return on assets by predicting  failures before they occur.
- Control cost of maintenance by enabling just-in-time maintenance operations.
- Lower customer attrition, improve brand image, and lost sales.
- Lower inventory costs by reducing inventory levels by predicting the reorder point.
- Discover patterns connected to various maintenance problems.
- Provide KPIs such as health scores for asset conditions.
- Estimate remaining lifespan of assets.
- Recommend timely maintenance activities.
- Enable just in time inventory by estimating order dates for replacement of parts.

These goal statements are the starting points for:

- _data scientists_ to analyze and solve specific predictive problems.
- _cloud architects and developers_ to put together the end to end solution.  

## Qualifying problems for PdM
It is important to emphasize that not all use cases or business problems can be effectively solved by PdM. There are three important qualifying criteria in problem selection:

- The problem has to be predictive in nature; that is, there should be a target or outcome to predict. The problem should have a clear path of action to prevent failures when they are detected.
- The problem should have a record of the operational history of equipment that contains _both good and bad outcomes_. The set of actions taken to mitigate bad outcomes should also be available as part of these records. Error reports, maintenance logs of performance degradation, repair, and replace logs are also very important.repairs undertaken to improve them, and replacement records are also useful.
- The recorded history should be reflected in _relevant_ data that is of _sufficient_ enough quality to support the use case. For more information about data relevance and sufficiency, see [Data Requirements for PdM](#Data-Requirements-for-PdM).
- Finally, the business should have domain experts who have a clear understanding of the problem. They should be aware of the internal processes and practices to be able to help the analyst understand and interpret the data. They should also be able to make the necessary changes to the business processes to help collect the right data for the problems.

## Sample PdM Use Cases
This section focuses on a collection of PdM use cases from several industries such as Aerospace, Utilities, and Transportation. Each section leads with a business problem, and discusses the benefits of PdM, the relevant data surrounding the business problem, and the benefits of a PdM solution.

| Business Problem | Benefits from PdM |
|:-----------------|-------------------|
|**Aviation** |                |
|_Flight delay and cancellations_ due to mechanical problems. Failures that cannot be repaired in time may cause flights to be cancel led, and disrupt scheduling and operations. |PdM solutions can predict the probability of an aircraft being delayed or canceled.|
|_Aircraft engine parts failure_: Aircraft engine part replacements are among the most common maintenance tasks in the airline industry. Maintenance solutions require careful management of component stock availability, delivery, and planning|Being able to gather intelligence on component reliability leads to substantial reduction on investment costs.|
|**Finance** |                         |
|_ATM failure_ is a common problem in the banking industry. The problem here is to calculate the probability that an ATM cash withdrawal transaction gets interrupted due to a paper jam or part failure in the cash dispenser. Based on predictions of transaction failures, ATMs can be serviced proactively to prevent failures from occurring| Rather than allow the machine to fail midway through a transaction, the better alternative is to program the machine to deny service based on the prediction.|
|**Energy** |                          |
|_Wind turbine failures_: Wind turbines are the main energy source in environmentally responsible countries like Norway and Germany, and involve high capital costs. A key component in wind turbines is the generator motor. Its failure renders the turbine ineffective and is expensive to fix|Predicting KPIs such as MTTF (mean time to failure) can help the energy companies prevent failures of the turbines with minimal downtime. Knowledge of the probability of failure can help technicians to focus on turbines that are likely to fail soon, and define time-based maintenance regimes. Predictive models provide insights into different factors that contribute to the failure,  which helps them better understand the root causes of the problems.|
|_Circuit breaker failures_: Distribution of electricity to homes and businesses requires power lines to be operational at all times to guarantee energy delivery. Circuit breakers help limit or avoid damage to power lines during overloading and adverse weather conditions. The business problem is to predict circuit breaker failures.| PdM solutions help reduce repair costs and increase the lifespan of equipment such as circuit breakers. They help improve the quality of the power network by reducing unexpected failures and service interruptions.|
|**Transportation and logistics** |    |
|_Elevator door failures_: Large elevator companies provide full stack services for millions of elevators around the world. Elevator safety, reliability, and uptime are the main concerns for their customers. These companies track these and other attributes via sensors, to help them with corrective and preventive maintenance. In an elevator, the most prominent customer problem is malfunctioning elevator doors. The business problem is to provide a knowledge base predictive application that predicts the potential causes of door failures.| Elevators are capital investments for potentially for 20-30 year lifespan of a building. So each potential sale can be highly competitive, and expectations for service and support are high. Predictive maintenance can provide these companies with an advantage over their competitors in product and service offerings.|
|_Wheel failures_: Wheel failures account for half of all train derailments and cost billions to the global rail industry. Wheel failures also cause rails to deteriorate, sometimes causing the rail to break prematurely. Rail breaks and help avoid catastrophic events such as derailments. To avoid such instances, railways monitor the performance of wheels and replace them in a preventive manner. The business problem here is the prediction of wheel failures.| Predictive maintenance of wheels will help with just-in-time replacement of wheels |
|_Subway train door failures_: A major reason for delays in subway operations is door failures of train cars. The business problem is to predict train door failures.|Early awareness of a door failure, or the number of days until a door failure, will help the business optimize train door servicing schedules.|

The next section gets into the details of how to realize the PdM benefits discussed above.

## **Data Science for Predictive Maintenance**

This section is organized as follows:
- [Data requirements for PdM](#Data-requirements-for-PdM)
- [Data preparation for PdM](#Data-preparation-for-PdM)
- [Feature Engineering](#Feature-Engineering)
- [Modeling techniques](#Modeling-techniques-for-PdM)
- [Model validation](#Model-Evaluation)

This section provides general guidelines of data science principles and practice for PdM. It is intended to help a TDM, solution architect, or a developer understand the prerequisites and process for building end-to-end AI applications for PdM. You can read this section side by side with a review of the demos and proof-of-concept templates listed in [Solution Templates for PdM](#Solution-Templates-for-PdM). You can then use these principles and best practices to implement your PdM solution in Azure.

> NOTE: This playbook does NOT teach Data Science. Several sources are provided
> in the [Appendix - Training in Data Science](#Appendix-Data-Science-training). 
> The > [solution templates listed in this playbook](#Solution-Templates-for-PdM) 
> demonstrate various techniques for a subset of the PdM problems. Newer techniques
> will be reflected in this playbook based on additions and state of the art.

## Data requirements for PdM

The success of any learning depends on (a) the quality of what is being taught (b) and the ability of the learner. Predictive models learn patterns from historical data, and predict future outcomes with certain probability based on these observed patterns. A model's predictive accuracy depends on the relevancy, sufficiency, and quality of the training and test data. The new data that is 'scored' using this model should have the same features and schema as the training/test data. The characteristics of each feature (type, density, distribution, and so on) should also match that of the training and test data sets. The focus of this section is on such data requirements.

#### _Relevant_ Data

First, the data has to be _relevant to the problem_. Consider the _wheel failure_ use case discussed above - the training data should contain features related to the wheel. If the problem was to predict the failure of the  _traction system_, the training data has to encompass all the different components for the traction system. The first case targets a specific component whereas the second case targets the failure of a larger subsystem. The general recommendation is to design prediction systems about specific components rather than larger subsystems, since the latter will have more dispersed data. The domain expert (see [Qualifying problems for PdM](#Qualifying-problems-for-PdM)) should help in selecting the most relevant subsets of data for the analysis. The relevant data sources are discussed in greater detail in [Data Preparation for PdM](#Data-preparation-for-PdM) 

#### _Sufficient_ Data
Two questions are commonly asked with regard to failure history data: (1) "How many failure events are required to train a model?" (2) "How many is considered as "enough"?" There are no definitive answers, but only rules of thumb. For (1), more the number of failure events, better the model. For (2),  and the exact number of failure events depends on the data and the context of the problem being solved. But on the flip side, if a machine fails too often then the business will replace it, which will reduce failure instances. Here again, the guidance from the domain expert matters. However, there are methods to cope with the issue of _rare events_. They are discussed in the section [Handling imbalanced data](#Handling-imbalanced-data).

#### _Quality_ Data
The quality of the data is critical - each predictor attribute value must be _accurate_ in conjunction with the value of the target variable. Data quality is a well-studied area in statistics and data management, and hence out of scope for this playbook.

> FURTHER READING: There are several resources and enterprise products to deliver quality data. A sample of references:
> - Dasu, T, Johnson, T., Exploratory Data Mining and Data Cleaning, Wiley, 2003.
> - [Exploratory Data Analysis, Wikipedia](https://en.wikipedia.org/wiki/Exploratory_data_analysis)
> - [Hellerstein, J, Quantitative Data Cleaning for Large Databases](http://db.cs.berkeley.edu/jmh/papers/cleaning-unece.pdf)
> - [de Jonge, E, van der loo, M, Introduction to Data Cleaning with R](https://cran.r-project.org/doc/contrib/de_Jonge+van_der_Loo-Introduction_to_data_cleaning_with_R.pdf)

## Data preparation for PdM

### Data sources

The relevant data sources for PdM are:
- Failure history
- Maintenance/Repair history
- Machine conditions through operational telemetry
- Equipment metadata

#### Failure History
Failure events are rare in PdM applications. However, when building prediction models, the algorithm needs to learn about a component's normal operational pattern, as well as its failure  patterns. So the training data should contain sufficient number of examples in both categories. Maintenance records and parts replacement history are good sources to find failure events. With the help of some domain knowledge, anomalies in the training data can also be defined as failures.

#### Maintenance/Repair History:
Maintenance history of an asset contains details about components replaced, repair activities performed etc. These events record degradation patterns. Absence of this crucial information in the training data can lead to wrong model results. Failure history is also be found within maintenance history as special error codes, or order dates for parts. Additional data sources that influence failure patterns should be provided by domain experts.

#### Machine conditions through operational telemetry
Sensor based (or other) telemetry of the equipment in operation is another data source. A key assumption in PdM is that a machine’s health status degrades over time during its operation. The data is expected to contain time-varying features that capture this aging pattern and any anomalies that leads to degradation. The temporal aspect of the data is required for the algorithm to learn the failure and non-failure patterns. Based on these learnings, the model can  predict how many more units of time a machine can continue to work before it fails.

#### Static feature data
Static features are metadata about the equipment such as technical specifications of make, model, manufactured date, date put into service, its location in the overall system, and so on.

Examples of relevant data for the [use cases](#Sample-PdM-Use-Cases) are tabulated below:

| Use Case | Examples of relevant data |
|:---------|---------------------------|
|_Flight delay and cancellations_ | Flight route information in the form of flight legs and page logs. Flight leg data includes routing details such as departure/arrival date, time, airports, etc. Page log data includes a series of error and maintenance codes that are recorded by the maintenance personnel. Maintenance records |
|_Aircraft engine parts failure_ | Telemetry data collected from sensors in the aircraft that provide information on the part's condition. Maintenance records help identify when component failures occurred and when they were replaced.|
|_ATM Failure_ | Sensor readings for each transaction and dispensing of each bill. Information on gap measurement between notes, note thickness, note arrival distance etc. Maintenance records that provide error codes and repair information.|
|_Wind turbine failure_ | Sensors monitor turbine conditions such as temperature, power, generator speed, and generator winding. Data for this use case will come from multiple wind turbines located in three different farm locations. Typically, each turbine will have 100+ sensor readings relaying measurements in 10-second intervals.|
|_Circuit breaker failures_ | Maintenance logs that include corrective, preventive, and systematic actions. Operational data that includes automatic and manual commands send to circuit breakers such as for open and close actions. Device metadata such as manufactured date, location, model, etc. Circuit breaker specifications such as voltage levels, geolocation, ambient conditions.|
|_Elevator door failures_| Elevator static features such as identifiers, contract maintenance frequency, building type. Usage information such as number of door cycles, average door close time. Failure history with causes.|
|_Wheel failures_ | Sensor data that measures wheel acceleration, braking instances, driving distance, velocity, and more. Static information on  vehicle features. Failure data inferred from part order database that  tracks order dates and quantities.|
|_Subway train door failures_ | Door opening and closing times, other operational data such as  current condition of doors. Static data would include asset identifier, time, and condition value columns.|

### Data Types
Given the above data sources, the two main data types observed in PdM domain are:

- **Temporal data**: Operational telemetry, machine conditions, work order types, priority codes, will have timestamps at the time of recording. Failure,  maintenance/repair, and usage history will also have timestamps for each event.
- **Static data**: Machine features and operator features in general are static since they describe the technical specifications of machines or operator’s properties. If these features could change over time, they should also have timestamps associated with them.

Predictor and target variables should be preprocessed/transformed into numerical, categorical, and other data types depending on the algorithm. For more information on data types, see [this site](https://www.statsdirect.com/help/basics/measurement_scales.htm).

### Data preprocessing
As a prerequisite to feature engineering, prepare the data from various streams to compose a schema from which it is easy to build features. Visualize the data as a table of records. Each row in the table represents a  training instance, and the columns represent _predictor_ features (also called independent attributes or variables). The last column(s) will be the  _target_ (dependent variable). For each training instance, assign a _label_ as the value of this column.

For temporal data, divide the duration of telemetry data into time units. Each record will belong to a time unit for an asset, _and will offer distinct information_. Time can be measured in units of seconds, minutes, hours, days, months, cycles. The time unit _does not have to be the same as the frequency of data collection_. If the frequency is high, the data may not show any significant difference from one unit to the other. For example, assume that ambient temperature was collected every 10 seconds. Using that same interval for training data only inflates the number of examples without providing any additional information. A better strategy would be to use average over tens of minutes, or an hour.

For static data, 
- _Maintenance records_: Raw maintenance data has an asset identifier and timestamp with information on maintenance activities that have been performed at a given time. Transform maintenance activities into _categorical_ columns, where each category descriptor uniquely maps to a maintenance action type. The schema for maintenance records would include asset identifier, time, and maintenance action.

- _Failure records_: Failures or failure reasons can be recorded as specific error codes or failure events defined by specific business condition. In cases where the equipment has multiple error codes, the domain expert should help identify the ones that are pertinent for the target variable. Use the remaining error codes or conditions to construct _predictor_ features that correlate with these failures. The schema for failure records would include asset identifier, time, failure, or failure reason - if it is available.

- _Machine and operator metadata_: Merge the machine and operator data into one schema to associate an asset with its operator, along with their respective attributes. The schema for machine conditions would include asset identifier, asset features, operator identifier, and operator features.

With the above preprocessed data sources in place, the final transformation before _feature engineering_ is to join the above tables based on asset identifer and time fields. The resulting table would have null values for the failure column when machine is in normal operation. These null values can be imputed by an indicator for normal operation. Use this failure column to create _labels for the predictive model_. For more information, see the section on [modeling techniques for PdM](#Modeling-techniques-for-PdM).

## Feature Engineering
Feature engineering is the first step in modeling. Conceptually, feature engineering abstracts a machine’s health using historical data that was collected up to a given point in time. This section discusses lag features that can be constructed from data sources with timestamps, and feature creation from static data sources. For more information, see [Feature Engineering](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/create-features).

### Lag features

Lag features are typically _numerical_ in nature, and are aggregated over specific windows of time. 

#### *Rolling aggregates*
For each record of an asset, a rolling window of size "W" is chosen as the number of units of time to compute the aggregates for. Lag features are then computed using the W periods _before the date_ of that record. In Figure 1, the blue lines show sensor values recorded for an asset for each unit of time. They denote a rolling average of feature values over a window of size W=3. Records with timestamps in the range t<sub>1</sub> (in orange) to t<sub>2</sub> (in green). The value for W is typically in minutes or hours. But for certain problems, picking a large W (say 12 months) can provide the whole history of an asset until the time of the record. 

![Figure 1. Rolling aggregate features](./media/cortana-analytics-playbook-predictive-maintenance/rolling-aggregate-features.png)

Figure 1. Rolling aggregate features

Examples of rolling aggregates over a time window are count, average, CUMESUM measures, min/max values. Variance, standard deviation, and count of outliers beyond N standard deviations are other examples. For some of the [use cases](#Sample-PdM-Use-Cases) in this playbook:
- _Flight delay prediction_: count of error codes over the past week.
- _Aircraft engine part failure_: rolling means, standard deviation, and sum over the past week, past three days, and past day.
- _ATM failures_: rolling means, median, range, standard deviations, count of outliers beyond three standard deviations, upper and lower CUMESUM.
- _Subway train door failures_: Count of events over past two weeks, past day, variance of count of events over past 15 days.
- _Circuit breaker failures_: Failure counts over past three years.

Another useful technique in PdM is to capture trend changes, spikes, and level changes using algorithms that detect anomalies in data.

#### *Tumbling aggregates*
For each labeled record of an asset, a window of size _W-<sub>k</sub>_ is defined, where _k_ is the number of windows of size _W_. Aggregates are then created over _k_ _tumbling windows_ _W-k, W-<sub>(k-1)</sub>, …, W-<sub>2</sub>, W-<sub>1</sub>_ for the periods before a record's timestamp. _k_ can be a small number to capture short-term effects, or a large number to capture long-term degradation patterns. (see Figure 2).

![Figure 2. Tumbling aggregate features](./media/cortana-analytics-playbook-predictive-maintenance/tumbling-aggregate-features.png)

Figure 2. Tumbling aggregate features

For the wind turbine use case, lag features could be created with W=1 and k=3 for each of the past three months using top and bottom outliers.

### Static features

Technical specifications of the equipment such as manufacture date, model number, location, are some examples of static features. They are treated as _categorical_ variables for modeling. For the circuit breaker use case, voltage, current, power capacity, transformer type, power source etc. are some examples. For wheel failures, the type of tire wheels (alloy vs steel) is an example.

Other feature engineering steps include **handling missing values** and **normalization** of attribute values - an exhaustive discussion is out of the scope of this playbook.

> FURTHER READING: A small sample from the many books/papers on feature engineering are listed below:
> - Pyle, D. Data Preparation for Data Mining (The Morgan Kaufmann Series in Data Management Systems), 1999
> - Zheng, A., Casari, A. Feature Engineering for Machine Learning: Principles and Techniques for Data Scientists, O'Reilly, 2018.
> - Dong, G. Liu, H. (Editors), Feature Engineering for Machine Learning and Data Analytics (Chapman & Hall/CRC Data Mining and Knowledge Discovery Series), CRC Press, 2018.

The data preparation efforts discussed so far should lead to the data being organized as shown below. Training, test, and validation data should have this logical schema (this example shows time in units of days). 

| Asset ID | Time | <Feature Columns> | Label |
| ---- | ---- | --- | --- |
| A123 |Day 1 | . . . | . |
| A123 |Day 2 | . . . | . |
| ...  |...   | . . . | . |
| B234 |Day 1 | . . . | . |
| B234 |Day 2 | . . . | . |
| ...  |...   | . . . | . |

The last step in feature engineering is **labeling** of the target variable. This process is dependent on the modeling technique, which in turn, depends on the business problem and nature of the available data. Labeling is disused in the next section.

## Modeling techniques for PdM

This section discusses the main modeling techniques for PdM problems, along with their specific label construction methods.

### Binary classification
Binary Classification is used to _predict the probability that a piece of equipment fails within a future time period_ - called the _future horizon period X_. X is determined by the business problem and the data at hand. Examples are:
- _minimum lead time_ required to replace components, deploy maintenance resources, perform  maintenance to avoid a problem that is likely to occur in that period.
- _minimum count of events_ that can happen before a problem occurs.

In this technique, two types of training examples are identified. A positive example, _which indicates a failure_, with label = 1. A negative example, which indicates normal operations, with  label = 0. The target variable, and hence the label values, are _categorical_. The model should identify each new example as likely to fail or work normally over the next X time units.

#### Label construction
The question here is: "What is the probability that the asset fails in the next X units of time?" To answer this question, label X records prior to the failure of an asset as "about to fail" (label = 1), and label all other records as "normal" (label =0). (see Figure 3).

![Figure 3. Labeling for binary classification](./media/cortana-analytics-playbook-predictive-maintenance/labelling-for-binary-classification.png)

Figure 3. Labeling for binary classification

Labeling strategy for some of the use cases:
- _Flight delays and cancellations_: X is chosen to be 1 day, to predict delays in the next 24 hours. All flights that are within 24 hours before failures are labeled with label = 1.
- _ATM cash dispense failures_: The goal is to determine failure probability of a transaction in the next 10 minutes. All transactions that happened within the past 10 minutes of the failure are labeled as 1. To predict failure probability in the next 100 notes dispensed, all notes dispensed within the last 100 notes of a failure are labeled as 1.
- _Circuit breaker failures_: Goal is to predict the next circuit breaker command failure. So  in which case X is chosen to be one future command.
- _Train door failures_: X chosen as seven days.
- _Wind turbine failures_: X chosen as three months.

### Regression for PdM
Regression models are used to _compute the remaining useful life (RUL) of an asset_. RUL is defined as the amount of time that the asset is operational before the next failure occurs. Each example is a record that belongs to a time unit _nY_ for an asset, where _n_ is the multiple. The model should calculate the RUL of each new example as a _continuous number_. This number denotes the period of time remaining before the failure.  

#### Label construction
The question here is: "What is the remaining useful life of the equipment?" For each record prior to the failure, calculate the label to be the number of units of time remaining before the next failure. In this method, labels are continuous variables. (See Figure 4)

![Figure 4. Labeling for regression](./media/cortana-analytics-playbook-predictive-maintenance/labelling-for-regression.png)

Figure 4. Labeling for regression

For regression, labeling is done with reference to a failure point. Its calculation is not possible without knowing how long the asset survived before failure. So in contrast to binary classification, assets without any failures in the data cannot be used for modeling. This issue is best addressed by another statistical technique called [Survival Analysis](https://en.wikipedia.org/wiki/Survival_analysis). But potential complications may arise when applying this technique to PdM use cases that involve time-varying data with frequent intervals. So Survival Analysis is not discussed in this playbook.

### Multi-class classification for PdM
Multi-class classification techniques can be used in PdM solutions for two scenarios:
- Predict _two future outcomes_: The first outcome is _a range of time to failure_ for an asset. The asset is assigned to one of multiple possible periods of time. The second outcome is the likelihood of failure in a future period due to _one of the multiple root causes_. This prediction enables the maintenance crew to watch for symptoms and plan maintenance schedules.
- Predict _the most likely root cause_ of a given failure. This outcome recommends the right set of maintenance actions to fix a failure. A ranked list of root causes and recommended repairs can help technicians prioritize their repair actions after a failure.

#### Label construction
The question here is: "What is the probability that an asset fails in the next _nZ_ units of time where _n_ is the number of periods?" To answer this question, label nZ records prior to the failure of an asset using buckets of time (3Z, 2Z, Z). Label all other records as "normal" (label = 0). In this method, the target variable holds _categorical_ values. (See Figure 5).

![Figure 5. Labeling for multiclass classification for failure time prediction](./media/cortana-analytics-playbook-predictive-maintenance/labelling-for-multiclass-classification-for-failure-time-prediction.png)

Figure 5. Labeling for multiclass classification for failure time prediction

The question here is: "What is the probability that the asset fails in the next Z units of time due to root cause/problem _RC<sub>i</sub>_?"_ where _i_ is the number of possible root causes. To answer this question, label Z records prior to the failure of an asset as "about to fail due to root cause _RC<sub>i</sub>_" (label = _RC<sub>i</sub>_). Label all other records as "normal" (label = 0). In this method also, labels are categorical (See Figure 6).

![Figure 6. Labeling for multiclass classification for root cause prediction](./media/cortana-analytics-playbook-predictive-maintenance/labelling-for-multiclass-classification-for-root-cause-prediction.png)

Figure 6. Labeling for multiclass classification for root cause prediction

The model assigns a failure probability due to each RC<sub>i</sub> as well as the probability of no failure. These probabilities can be ordered by magnitude to allow prediction of the problems that are most likely to occur in the future.

The question here is: "What maintenance actions do you recommend after failures?" To answer this question, labeling _does not_ require a future horizon to be picked, because the model is not predicting failure in the future. It is just predicting the most likely root cause _once the failure has already happened_. 

## Modeling Techniques applies to PdM Use Cases

This section shows how the modeling techniques and labeling strategies are applied to the [Sample PdM Use Cases](#Sample-PdM-Use-Cases).

| Use Case | Modeling Technique | Label construction |
|:---------|--------------------|--------------------|
|_Flight delay and cancellations_ | Multi-class classification model to predict the type of mechanical issue that causes a flight delay or cancellation in the next X hours. | Choose X = 1 day to predict delays in the next 24 hours. Label flights that are within 24 hours before failures with label = 1. |
|_Aircraft engine parts failure_ | Multi-class classification model that predicts the probability of failure of a component in the next N days | |
|_ATM Failure_ | Two separate binary classification models - the first one to predict transaction failures and the second to predict cash dispensing failures. Failure prediction could be failure in two areas: failure probability of a transaction in the next 10 minutes, and probability of failure in the next 100 notes dispensed. |All transactions that happened within the last 10 minutes of the failure are labeled as 1 for the first model. All notes dispensed within the last 100 notes of a failure were labeled as 1 for the second model.|
|_Wind turbine failure_ | |X was chosen as 3 months.|
|_Circuit breaker failures_ | Probability that the next circuit breaker command fails in which case X is chosen to be one future command.| |
|_Elevator door failures_|A multiclass logistic regression model to predict the cause of the failure given historical data on operating conditions. This model is then used to predict the most likely root causes after a failure has occurred.| |
|_Wheel failures_ | | |
|_Subway train door failures_ |For train door failures, the binary classification model was built to predict failures within the next 7 days. | |

## Training, validation, and testing methods for PdM
The [Team Data Science Process](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/overview) provides a full coverage of the model train-test-validate cycle. This section discusses aspects unique to PdM.

### Cross validation
The goal of [cross validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)) is to define a dataset to "test" the model in the training phase. This data set is called the  _validation set_. This technique helps limit problems like _overfitting_ and gives an insight on how the model will generalize to an independent dataset. That is, an unknown dataset, which could be from a real problem. The training and testing routine for PdM needs to take account the time varying aspects to better generalize on unseen future data.

Many machine learning algorithms depend on a number of hyperparameters that can change model performance significantly. The optimal values of these hyperparameters are not computed automatically when training the model. They should be specified by data scientist. There are several ways of finding good values of hyperparameters. The most common one is _k-fold cross-validation_ that splits the examples randomly into _k_ folds. For each set of hyperparameters values, run the learning algorithm _k_ times. At each iteration, use the examples in the current fold as a validation set, and the rest of the examples as a training set. Train the algorithm over training examples and compute the performance metrics over validation examples. At the end of this loop, compute the average of _k_ performance metrics For each set of hyperparameter values. Choose the hyperparameter values that have the best average performance.

In PdM problems, data is recorded as a time series of events that come from several data sources. These records may be ordered according to the time of labeling. Hence, if the dataset is split _randomly_ into training and validation set, _some of the training examples may be later in time than some of validation examples_. Future performance of hyperparameter values will be estimated based on some data that arrived _before_ model was trained. These estimations might be overly optimistic, especially if time-series are not stationary and evolve over time. As a result, the chosen hyperparameter values might be suboptimal.

The recommended way is to split the examples into training and validation set in a _time-dependent_ manner, where all validation examples are later in time than all training examples. For each set of hyperparameter values, train the algorithm over the training data set. Measure the model’s performance over the same validation set. Choose hyperparameter values that show the best performance. Hyperparameter values chosen by train/validation split result in better future model performance than with the values chosen randomly by cross-validation.

The final model can be generated by training a learning algorithm over entire training data using the best hyperparameter values.

### Testing for model performance
Once a model is built, an estimate of its future performance on new data is required. The simplest estimate could be the performance of the model over the training data. But this estimate is overly optimistic, because the model is tailored to the data that is used to estimate performance. A better estimate could be the performance metric of hyperparameter values computed over the validation set, or an average performance metric computed from cross-validation. But for the same reasons as previously stated, these estimations are still overly optimistic. A more realistic approach for measuring model performance is required.

The recommended way for PdM is to split the examples into training, validation, and test sets in a time-dependent manner. All test examples should be later in time than all the training and validation examples. After the split, generate the model and measure its performance as described earlier.

When time-series are stationary and easy to predict, both random and time-dependent approaches generate similar estimations of future performance. But when time-series are non-stationary, and/or hard to predict, the time-dependent approach will generate more realistic estimates of future performance.

### Time-dependent split
This section describes best practices to implement time-dependent split. A time-dependent two-way split between training and test sets is described. The same logic can be applied
for time-dependent split for training and validation sets.

Assume a stream of timestamped events such as measurements from various sensors. Define features and labels of training and test examples over timeframes that contain multiple events. For example, for binary classification, create features based on past events, and create labels  based on future events within "X" units of time in the future (see the sections on [feature Engineering](#Feature-Engineering) and [modeling techniques](#Modeling-Techniques-applied-to-PdM-Use-Cases)). Thus, the labeling timeframe of an example comes later than the timeframe of its features.

For time-dependent split, pick a _training cutoff time T<sub>c</sub>_ at which to train a model, with hyperparameters tuned using historical data up to T<sub>c</sub>. To prevent leakage of future labels that are beyond T<sub>c</sub> into the training data, choose the latest time to label training examples to be X units before T<sub>c</sub>. In the example shown in Figure 7, each square represents a record in the data set where features and labels are computed as described above. The figure shows the records that should go into training and testing sets for X=2 and W=3:

![Figure 7. Time-dependent split for binary classification](./media/cortana-analytics-playbook-predictive-maintenance/time-dependent-split-for-binary-classification.png)

Figure 7. Time-dependent split for binary classification

The green squares represent records belonging to the time units that can be used for training. Each training example is generated by considering the past three periods for feature generation, and two future periods for labeling before T<sub>c</sub>. When any part of the two future periods is beyond T<sub>c</sub>, exclude that example from the training dataset because no visibility is assumed beyond T<sub>c</sub>.

The black squares represent the records of the final labeled dataset that should not be used in the training data set, given the above constraint. These records won’t be used in testing data either since they are before T<sub>c</sub>. In addition, their labeling timeframes partially depend on the training timeframe, which is not ideal. Training and test data should have separate labeling timeframes to prevent label information leakage.

The technique discussed so far allows for overlap between training and testing examples that have timestamps near T<sub>c</sub>. A solution to achieve greater separation is to exclude examples that are within W time units of T<sub>c</sub> from the test set. But such an aggressive split depends on ample data availability.

Regression models used for predicting RUL are more severely affected by the leakage problem. Using the random split method leads to extreme overfitting. For regression problems, the split should be such that the records belonging to assets with failures before T<sub>c</sub> into the training set. Records of assets that have failures after the cutoff go into the test set.

Another best practice for splitting data for training and testing is to use a split by asset ID. The split should be such that none of the assets used in the training set are used in testing the model performance. Using this approach, a model has a better chance of providing more realistic results with new assets.

### Handling imbalanced data
In classification problems, if there are more examples of one class than of the others, the data is said to be imbalanced. Ideally, enough representatives of each class in the training data are preferred to enable distinction between different classes. If one class is less than 10% of the data, the data is deemed to be imbalanced. The underrepresented class is called a _minority class_. Many PdM problems face such imbalanced datasets, where one class is severely underrepresented compared to others. In some situations, the minority class may constitute only 0.001% of the total data points. Class imbalance is not unique to PdM; other domains such as fraud detection and network intrusion, where failures and anomalies are rare occurrences, face this problem. These failures make up the minority class examples.

With class imbalance in data, performance of most standard learning algorithms is compromised, since they aim to minimize the overall error rate. For a data set with 99% negative and 1% positive examples, a model can be shown to have 99% accuracy by labeling all instances as negative. But the model will misclassify all positive examples; so even if its accuracy is high, the algorithm is not a useful one. Consequently, conventional evaluation metrics such as _overall accuracy on error rate_ are insufficient for imbalanced learning. When faced with imbalanced datasets, other metrics are used for model evaluation:
- Precision
- Recall
- F1 scores
- Cost adjusted ROC (receiver operating characteristics)

For more information about these metrics, see [Model Evaluation Metrics](#Model-Evaluation).

However, there are some methods that help remedy class imbalance problem. The two major ones are _sampling techniques_ and _cost sensitive learning_.

#### Sampling methods
Imbalanced learning involves the use of sampling methods to modify the training dataset to a balanced dataset. Sampling methods are not to be applied to the test set. Although there are several sampling techniques, most straight forward ones are _random oversampling_ and _under sampling_.

_Random oversampling_ involves selecting a random sample from minority class, replicating these examples, and adding them to training data set. Consequently, the number of examples in minority class is increased, and eventually balance the number of examples of different classes. A drawback of oversampling is that multiple instances of certain examples can cause the classifier to become too specific, leading to overfitting. The model may show high training accuracy, but its performance on unseen test data may be suboptimal.

Conversely, _random under sampling_ is selecting a random sample from majority class and removing those examples from training data set. However, removing examples from majority class may cause the classifier to miss important concepts pertaining to the majority class. _Hybrid sampling_ where minority class is oversampled and majority class is undersampled at the same time is another viable approach.

There are many sophisticated sampling techniques. The technique chosen depends on the data properties and results of iterative experiments by the data scientist.

#### Cost sensitive learning
In PdM, failures that constitute the minority class are of more interest than normal examples. So the focus is mainly on algorithm performance on failures. Incorrectly predicting a positive class as a negative class can cost more than vice versa. This situation is commonly referred as unequal loss or asymmetric cost of misclassifying elements of different classes. The ideal classifier should deliver high prediction accuracy over the minority class, without compromising on the accuracy for the majority class.

There are multiple ways to achieve this balance. To mitigate the problem of unequal loss, assign a high cost to misclassification of the minority class, and try to minimize the overall cost. Algorithms like _SVMs (Support Vector Machines)_ adopt this method inherently, by allowing cost of positive and negative examples to be specified during training. Similarly, boosting methods such as _boosted decision trees_ usually show good performance with imbalanced data. 

## Model Evaluation
Misclassification is a significant problem for PdM scenarios where the cost of false alarms to the business is high. For instance, a decision to ground an aircraft based on an incorrect prediction of engine failure can disrupt schedules and travel plans. Taking a machine offline from an assembly line can lead to loss of revenue. So model evaluation with the right performance metrics against new test data is critical.

Typical performance metrics used to evaluate PdM models are discussed below:

- [Accuracy](https://en.wikipedia.org/wiki/Accuracy_and_precision) is the most popular metric used for describing a classifier’s performance. But accuracy is sensitive to data distributions, and is an ineffective measure for scenarios with imbalanced data sets. Other metrics are used instead. Tools like [confusion matrix](https://en.wikipedia.org/wiki/Confusion_matrix) are used to compute and reason about accuracy of the model.
- [Precision](https://en.wikipedia.org/wiki/Precision_and_recall) of PdM models relate to the rate of false alarms. Lower precisions of the model generally correspond to a higher rate of false alarms.
- [Recall](https://en.wikipedia.org/wiki/Precision_and_recall) rates denote how many of the failures in the test set were correctly identified by the model. Higher recall rates mean the model is successful in catching the true failures.
- [F1 score](https://en.wikipedia.org/wiki/F1_score) is the harmonic average of precision and recall, with its value ranging between 0 (worst) to 1 (best).
  both precision and recall rates with best value being 1 and worst being 0.

For binary classification,
- [Receiver operating curves (ROC)](https://en.wikipedia.org/wiki/Receiver_operating_characteristic) are a popular metric. In ROC curves, model performance is interpreted based on one fixed operating point on the ROC. But for PdM problems, _decile tables_ and _lift charts_ are more informative. They focus only on the positive class (failures), and provide a more complex picture of the algorithm performance than ROC curves. the ROC.
- _Decile tables_ are created using test examples in a descending order of  failure probabilities. The ordered samples are then grouped in deciles (10% of the samples with highest probability, then 20%, 30%, and so on). The ratio (true positive rate)/(random baseline) for each decile helps estimate the algorithm performance at each decile. the random baseline takes on values 0.1, 0.2, and so on.
- _Lift charts_ plot decile true positive rate versus random true positive rate for all deciles. The first deciles show the largest gains. Hence, they are usually the focus of results. First deciles can also be seen as representative for "at risk" when used for PdM.

## Model operationalization for PdM

**T B D**

## **Solution Templates for PdM**

The final section of this playbook provides a list of PdM solution templates, tutorials, and experiments implemented in Azure. These PdM applications can be deployed into an Azure subscription within minutes to hours. They can be used as proof-of-concept demos, sandboxes to experiment with alternatives, or accelerators for actual production implementations. These templates are located in the [Azure AI Gallery](http://gallery.azure.ai), or at GitHub (https://github.com/Azure).

| Solution Template Title | Description |
|:------------------------|-------------|
|[Azure Predictive Maintenance Machine Learning Sample](https://github.com/Azure/MachineLearningSamples-PredictiveMaintenance) |PdM sample that demonstrates use of latest Azure ML on DSVM on sample CSV data. Ideal for beginners to PdM.|
|[Azure Predictive Maintenance Solution Template](https://github.com/Azure/AI-PredictiveMaintenance) | An end to end, scalable, pr
|[Azure AI Toolkit for IoT Edge](https://github.com/Azure/ai-toolkit-iot-edge) | AI in the IoT edge using TensorFlow; toolkit packages deep learning models in Azure IoT Edge-compatible Docker containers and expose those models as REST APIs.
| [Azure Predictive Maintenance for Aerospace](https://gallery.azure.ai/Solution/Predictive-Maintenance-for-Aerospace-1) | One of the first PdM solution templates based on Azure ML v1.0 for aircraft maintenance. This playbook originated from this project |
| [Azure IoT Predictive Maintenance](https://github.com/Azure/azure-iot-predictive-maintenance) | Azure IoT Suite PCS - Preconfigured Solution. Aircraft maintenance PdM template with IoT Suite |
|[Predictive Maintenance Modeling Guide in R](https://gallery.azure.ai/Notebook/Predictive-Maintenance-Modelling-Guide-R-Notebook-1) | PdM modeling guide in Azure ML v1.0 |

# Appendix

## PdM Microsoft Documentation links and blog posts

ToDo

## Data Science Training Resources

ToDo