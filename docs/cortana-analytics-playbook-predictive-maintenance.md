---
title: Azure Cloud AI Playbook for Predictive maintenance solution templates | Microsoft Docs
description: A Solution Template with Microsoft Azure ML for Predictive Maintenance in aerospace, utilities, and transportation.
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
# Azure Cloud AI Playbook for Predictive Maintenance (PdM)
_Contributors: [Fidan Boylu Uz, PhD](https://github.com/fboylu), [Gary Ericson](https://github.com/garyericson); [Ramkumar Krishnan](https://github.com/ramkumarkrishnan)_

## Summary
Predictive maintenance (abbreviated as PdM) is a popular application of predictive analytics given its promise to deliver high ROI and cost savings to manufacturing, services, retail and other industries.

This playbook provides a reference for PdM solutions for a set of common use cases. It gives the reader an understanding of the common business scenarios for PdM, challenges in qualifying business problems, the data required to solve these problems, predictive modeling techniques to build solutions using such data, and technology best practices with solution templates, reference architectures and implementations. It describes the data science process behind building predictive models - such as feature engineering, model development and performance evaluation. In essence, this playbook brings together the business and analytical guidelines needed for a successful development and deployment of PdM solutions using the [Microsoft Azure AI platform](https://azure.microsoft.com/en-us/overview/ai-platform).

### Playbook overview and target audience
The first half of this playbook will benefit business decision makers (BDMs) interested in understanding the solution space by describing typical business problems, the benefits of implementing PdM to address these problems, and a list of common use cases. The second half of the playbook will benefit technical decision makers (TDMs) by describing the data science behind PdM in general terms, and providing pointers to several PdM solution template implementations using Microsoft Azure.

| Start with ... | If you are ... |
|:---------------|:---------------|
| [Business case for PdM](#Business-Case-for-PdM) |a business decision maker (BDM) looking to reduce downtime and operational costs, and improving utilization of  equipment | 
| [Data Science for PdM](#Data-Science-for-PdM) |a technical decision maker (TDM) evaluating PdM technologies to understand the unique data processing and AI requirements for predictive maintenance |
| [Solution Templates for PdM](#Solution-Templates-for-PdM)|a sofware architect or AI Developer looking to quickly stand up a demo or proof-of-concept | 

### Prerequisite knowledge
The BDM content requires none to little prior knowledge of data science. The TDM content requires introductory to intermediate level knowledge of statistics and data science, and intermediate level to advanced knowledge of Azure Data and AI services. _Python_ and/or _R_ dominate the hands-on practice of data science. Solution templates are implemented in Azure predominantly using _.Net_, with a few examples in _Node.js_, and _Java_; knowledge of _Powershell_ and _JSON_ is useful. The playbook provides ample pointers to training and documentation in these areas.

## **Business Case for Predictive Maintenance**

This section is organized as follows:

- [Business Problems in PdM](#Business-Problems-in-PdM)
- [Qualifying problems for PdM](#Qualifying-problems-for-PdM)
- [Sample PdM Use cases](#Sample-PdM-Use-Cases)

Businesses require critical equipment and assets - from specialized equipment such as aircraft engines, turbines, and industrial chillers down to familiar equipment like elevators and xray machines - to be running at peak efficiency and utilization to realize ROI.
- By default, most businesses rely on _corrective maintenance_, where parts are replaced as they fail. Corrective maintenance ensures parts are used completely (not wasting component life), but costs the business both in downtime and unscheduled maintenance requirements (off hours, or inconvenient locations).
- The next alternative is a _preventive maintenance_ - where businesses may track or test component failures to determine a safe lifespan of a component, and replace it before a costly failure. This avoids unscheduled failures, and ensures that safety critical machinery have no catastrophic failures. But the high costs of scheduled downtime, under-utilization of the component before its full lifetime of use, and labor still remain.
- The goal of _predictive maintenance_ is to optimize the balance between corrective and preventative maintenance, by enabling _just in time_ replacement of components. This approach only replaces those components when they are close to failure. The savings come from both extending component lifespans (compared to preventive maintenance), reducing unscheduled maintenance and labor costs (over corrective maintenance), offering businesses a competitive edge over their peers with traditional maintenance procedures.

## Business Problems in PdM
Business problems in the PdM domain range from high operational risk due to unexpected failures and limited insight into the root cause of problems in complex business environments. The majority of these problems can be categorized to fall under the following business questions:

- Detect anomalies in equipment or system performance or functionality
- Predict that an equipment may fail in the near future
- Estimate the remaining useful life of an equipment
- Identify the main causes of failure of an equipment
- Identify what maintenance actions need to be done, by when, on an asset

The typical business expectations ("PdM can help me ...") or goal statements for the TDM are the following:

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

- _data scientists_ to analyze, define and solve  specific predictive problems.
- _cloud architects and developers_ to put together the end to end solution.  

## Qualifying problems for PdM
It is important to emphasize that not all use cases or business problems can be effectively solved by PdM. There are three important qualifying criteria in problem selection:

- The problem has to be predictive in nature; that is, there should be a identifiable target or outcome to predict. As a baseline, the problem should have a clear path of (corrective or preventive) action to prevent failures when they are detected.
- The problem should have a recorded history of past behavior of the equipment with _both good and bad outcomes_; along with the set of actions taken to mitigate the bad outcomes. Error reports and maintenance logs of performance degradation, repairs undertaken to improve them, and records of replacements are also useful.
- The recorded history should be reflected in _relevant_ data that is of _sufficient_ enough quality to support the use case. More on this under [Data-Requirements-for-PdM](#Data-Requirements-for-PdM)
- Finally, and importantly, the business should have domain experts who have a very clear understanding of the problem, the processes, practices, and documented or undocumented hueristics that can help the AI developer understand and interpret the data, and also know how to help correct the deficiencies in the data.

No amount of data science or AI technology can sufficiently and correctly solve the business problem without these prerequisites.

## Sample PdM Use Cases
This section focuses on a collection of PdM use cases from several industries such as Aerospace, Utilities and Transportation. Each section leads with a business problem, and discusses the benefits of PdM, the relevant data surrounding the business problem, and the benefits of a PdM solution.

| Business Problem | Benefits from PdM |
|:-----------------|-------------------|
|**Aviation** |                |
|_Flight delay and cancellations_ due to mechanical problems. Failures that cannot be repaired in time may cause flights to be cancelled, resulting in cascading problems in scheduling and operations, leading to loss of reputation and customer dissatisfaction|PdM solutions can predict the probability of an aircraft being delayed or canceled.|
|_Aircraft engine parts failure_: Aircraft engine part replacements are among the most common maintenance tasks in the airline industry. Maintenance solutions require careful management of component stock availability, delivery and planning|Being able to gather intelligence on component reliability leads to substantial reduction on investment costs.|
|**Finance** |                         |
|_ATM failure_ is a common problem in the banking industry. The problem here is to calculate the probability that an ATM cash withdrawal transaction gets interrupted due to a paper jam or part failure in the cash dispenser. Based on predictions of transaction failures, ATMs can be serviced proactively to prevent failures from occurring|Preemptive awareness of cash dispensing failures can be used to program the machine to refuse service, rather than inconvenience a customer with an incomplete transaction|
|**Energy** |                          |
|_Wind turbine failures_: Wind turbines are the main energy source in environmentally responsible countries like Norway and Germany, and involve high capital costs. A key component in wind turbines is the generator motor. Its failure renders the turbine ineffective and is expensive to fix|Predicting KPIs such as MTTF (mean time to failure) can help the energy companies prevent failures of the turbines with minimal downtime. Knowledge of the probability of failure can help technicians to focus on turbines that are likely to fail soon, and define time-based maintenance regimes. Predictive models provide insights into different factors that contribute to the failure,  which helps them better understand the root causes of the problems.|
|_Circuit breaker failures_: Generation, distribution and sale of electricity to homes and businesses require regular maintenance to ensure that power lines are operational at all times to guarantee energy delivery. Circuit breakers are a critical component in avoiding or limiting damage to power lines during overloading and adverse weather conditions. The business problem is to predict circuit breaker failures.| PdM solutions help reduce repair costs and increase the lifespan of equipment such as circuit breakers. They help improve the quality of the power network by reducing unexpected failures and service interruptions.|
|**Transportation and logistics** |    |
|_Elevator door failures_: Large elevator companies provide full stack services for millions of elevators around the world. Elevator safety, reliability, and uptime are the main concerns for their customers. These companies track these and other attributes via sensors, to help them with corrective and preventive maintenance. In an elevator, the most prominent customer problem is malfunctioning of of elevator doors. The business problem is to provide a knowledge base predictive application that predicts the potential causes of door failures.| Elevators are one-time sales potentially for 20-30 year lifespan - so there is a lot of pre-sales customer scrutiny and competition for each sale. Predictive maintenance can provide these companies with a technological differentiation and edge over their competitors in this highly capital intensive, white glove service based industry.|
|_Wheel failures_: Wheel maintenance for trains and heavy industrial vehicles are typically corrective or preventive, which have the inefficiencies stated in the introduction. The business problem here is the prediction of wheel failures| Predictive maintenance of wheels will help with in time replacement, translating to savings and time saved for customers, and avoiding the inconvenience of unexpected failures|
|_Subway train door failures_: A major reason for delays in subway operations is door failures of train cars. The business problem is to predict train door failures|Predicting if a train car may have a door failure, or being able to forecast the number of days till the next door failure provides the business the opportunity to optimize train door servicing and reduce the train's down time.|

The next section gets into the details of how to realize the PdM benefits discussed above.

## **Data Science for Predictive Maintenance**

This section is organized as follows:
- [Data requirements for PdM](#Data-requirements-for-PdM)
- [Data preparation for PdM](#Data-preparation-for-PdM)
- [Feature Engineering](#Feature-Engineering)
- [Modeling techniques](#Modeling-Techniques)
- [Model validation](#Model-Validation)

This section provides general guidelines of data science principles and practice for PdM. It begins by listing the data requirements, and walks through data preparation, feature engineering, modeling techniques, model validation, and model operationalization (i.e. scoring new data with the model). It is intended to help a TDM, solution architect or a developer think through the prerequisites and process for building end to end AI applications for PdM. You can read this section side by side while reviewing the demos and proof-of-concept templates listed in the section [Solution Templates for PdM](#Solution-Templates-for-PdM), and use these principles and best practices to implement your PdM solution in Azure.

> NOTE: This playbook does NOT teach Data Science. Several sources are provided
> in the [Appendix - Training in Data Science](#Appendix-Data-Science-training). 
> also is not a directory of all AI techniques for PdM. The
> [solution templates listed in this playbook](#Solution-Templates-for-PdM) 
> demonstrate some or all of these techniques discussed here - newer techniques
> will be reflected in this playbook based on additions and state of the art.

## Data requirements for PdM

The success of any learning depends on (a) the quality of what is being taught (b) and the ability of the learner. Predictive models learn patterns from historical data, and predict future outcomes with certain probablity based on these observed patterns. A model's predictive accuracy depends on the relevancy, sufficiency, and quality of the training and test data; and a requirement  that the new data match the training/test data in all data characteristics (type, density, distribution, and so on). This section lists those key data requirements.

#### _Relevant_ Data

First, the data has to be _relevant to the problem_. Consider the _wheel failure_ use case discussed above - the training data should contain features related to the wheel. If the problem was to predict the failure of the  _traction system_, the training data has to encompass all the different components for the traction system. The first case targets a specific component whereas the second case targets the failure of a larger subsystem. The general recommendation is to design prediction systems about specific components rather than larger subsystems, beaue teh later will have more dispersed data. The domain expert (see [Qualifying problems for PdM](#Qualifying-problems-for-PdM)) should help in selecting the most relevant subsets of data for the analysis. The relevant data sources are discussed in greater detail in [Data Preparation for PdM](#Data-preparation-for-PdM) 

#### _Sufficient_ Data
A common question about failure history data is "How many failure events are required to train a model and how many is considered as "enough"? If a machine fails too often, then it will be a risk for the business to not replace it, and that reduces the failure instances. The rule of thumb answer is that the more the number of failure events the better the model is, adn the exact number depends on the data and the context of the problem being solved. Here again, the guidance from the domain expert matters. There are however methods to cope with this issue of _rare events_, and they are discussed in the section [Handling imbalanced datasets](Handling-imbalanced-datasets).

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
Failure events are rare in PdM applications. However, when building models to predict failures, the algorithm needs to learn both the normal operation pattern as well as the failure pattern. Hence, it is essential that the training data contains sufficient number of examples in both categories. Failure events can be found in maintenance records and parts replacement history. Domain experts can help define certain anomalies in the training data as failures.

#### Maintenance/Repair History:
Maintenance history of the asset contains information about the components replaced, preventive maintenance activates performed, etc. These events record degradation patterns. Absence of this information can cause misleading results. Failure history is often contained in maintenance history in the form of special error codes or order dates for spare parts. In such cases, failures can be extracted from the maintenance data. Additional data sources that influence failure patterns should be provided by domain experts.

#### Machine conditions through operational telemetry
Sensor based (or other) telemetry of the equipment in operation is another data source. A key assumption in PdM is that a machine’s health status degrades over time during its operation. The data is expected to contain time-varying features that capture this aging pattern and any anomalies that leads to degradation. This temporal aspect of the data is required for the algorithm to learn the failure and non-failure patterns and predict how many more units of time (hours, days) a machine can continue to work before it fails.  before it fails, we assume the 

#### Static feature data
Static features are metadata about the equipment such as technical specifications of make, model, manufactured date, date put into service, its location in the overall system, and so on.

Examples of relevant data for the [use cases](#Sample-PdM-Use-Cases) are tabulated below:

| Use Case | Examples of relevant data |
|:---------|---------------------------|
|_Flight delay and cancellations_ | Flight route information in the form of flight legs and page logs. Flight leg data includes routing details such as departure/arrival date, time, airports, etc. Page log data includes a series of error and maintenance codes that are recorded by the maintenance personnel. Maintenance records |
|_Aircraft engine parts failure_ | Telemetry data collected from a number of sensors in the aircraft providing information on the condition of the part. Maintenance records that help identify when component failures occurred and when they were replaced.|
|_ATM Failure_ | Sensor readings that track each transaction, and the dispensing of each bill, and measure gaps between notes, thickness, note arrival distance etc. Maintenance records that provide error codes and repair information.|
|_Wind turbine failure_ | Sensors monitor turbine conditions such as temperature, generator speed, turbine power and generator winding. Data for this use case comes from multiple wind turbines located in three different farm locations, with 100+ sensor readings per turbine recording and relaying measurements in 10 second intervals.|
|_Circuit breaker failures_ | Maintenance logs that include corrective, preventive and systematic actions, operational data that includes automatic and manual commands send to circuit breakers such as for open and close actions, and technical specification data about the properties of each circuit breaker such as manufactured date, location, model, etc. Circuit breaker technical specifications such as voltage levels, geolocation, ambient conditions.|
|_Elevator door failures_| Relevant data is in three parts - Elevator static features (e.g. identifiers, contract maintenance frequency, building type, etc.), usage information (e.g. number of door cycles, average door close time, etc.) and failure history (i.e. historical failure records and their causes).|
|_Wheel failures_ | Sensor data that measures wheel acceleration, braking instances, driving distance, velocity, etc. along with other static information such as vehicle features, failure data inferred from part order database which tracks spare part order dates and quantities as vehicles are being serviced.|
|_Subway train door failures_ | Door opening and closing times, other operational data such as  current condition of doors. Static data would include asset ID, time and condition value columns.|

### Data Types
Given the above data sources, the two main data types we observe in PdM domain are:

- **Temporal data**: Operational telemetry from sensors and failure history, machine conditions, maintenance/repair history, work order types, priority codes, usage history will have timestamps at the time of recording.
- **Static data**: Machine features and operator features in general are static since they usually describe the technical specifications of machines or operator’s properties. If these features could change over time, they should also have timestamps associated with them.

Further, depending on the predictive technique, predictor and target variables will need to be preprocessed/transformed into numerical, categorical and other data types for measurement scales. See [here](https://www.statsdirect.com/help/basics/measurement_scales.htm) for more details.

### Data preprocessing
As a prerequisite to feature engineering, the data from various streams must be prepared to compose a schema from which it is easy to build features. Visualize the data as a set of records, with each row representing one training instance, and with all but one column representing _predictor_ features (also called independent attributes or variables) and the remaining column being the _target_ (dependent variable). 

For temporal data, divide the duration of telemetry data into time units where each record belongs to a time unit for an asset, _and offers distinct information_. Time can be measured in units of seconds, minutes, hours, days, months, cycles. The time unit _does not have to be the same as the frequency of data collection since the data may not show any difference from one unit to the other_. For example, if ambient temperature was collected every 10 seconds, picking a time unit of 10 seconds for the whole analysis only inflates the number of examples without providing any additional information. A better strategy would be to use average over an hour.

For static data, 
- _Maintenance records_: Raw maintenance data usually comes with an Asset ID and timestamp with information about what maintenance activities have been performed at that time. These maintenance activities have to transformed into _categorical_ columns, where each category descriptor uniquely maps to a a maintenance action type. The schema for maintenance records would include asset ID, time and maintenance action.

- _Failure records_: Failures or failure reasons can be recorded as specific error codes or failure events defined by specific business condition. In cases where the equipment has multiple error codes, the domain expert should help identify only those that pertinent for the target variable. the remaining error codes or conditions can be used to construct _predictor_ features that correlate with these failures. The schema for failure records would include asset ID, time and failure or failure reason columns if reason is available.

- _Machine and operator metadata_: Machine and operator data could be merged into one schema to identify which asset was operated by which operator along with asset and operator properties. The schema for machine conditions would include asset ID, asset features, operator ID and operator features.

With the above preprocessed data sources in place, the final transformation before _feature engineering_ is to join the above tables based on Asset ID and Time fields. The resulting table would have null values for failure column when machine is in normal operation. These can be imputed by an indicator value for normal operation. This failure column is used to create _labels for the predictive model_.

## Feature engineering
Feature engineering is the first step in modeling. The idea of feature generation is to conceptually describe and abstract a machine’s health condition at a given time using historical data that was collected up to that point in time. In this section, we discuss lag features that can be constructed from data sources with timestamps, and features creation from static data sources. Refer to this Microsoft documentation for general information on [Feature Engineering](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/create-features).

### Lag features

Lag features are typically _numerical_ in nature, and are aggregated over specific windows of time. 

#### *Rolling aggregates*
For each record of an asset, we pick a rolling window of size "W" as the number of units of time that we would like to compute the aggregates for. We then compute rolling aggregate features using the W periods _before the date_ of that record. In Figure 1, we represent sensor values recorded for an asset for each unit of time with the blue lines and mark the rolling average feature calculation for W=3 for the records at t<sub>1</sub> (in orange) and t<sub>2</sub> (in green). These aggregate windows are typically in the range of minutes or hours. But in certain cases, picking a large W (say 12 or 18 month cycles) can provide the whole history of an asset until the time of the record. 

![Figure 1. Rolling aggregate features](./media/cortana-analytics-playbook-predictive-maintenance/rolling-aggregate-features.png)

Figure 1. Rolling aggregate features

Examples are rolling counts, means, standard deviations, outliers based on standard deviations, CUMESUM measures, minimum and maximum values for the window. For some of the [use cases](#Sample-PdM-Use-Cases) in this playbook:
- _Flight delay prediction_: counts of error codes from last week were used to create features.
- _Aircraft engine part failure_: sensor values from last week, last three days and last day were used to create rolling means, standard deviation and sum features.
- _ATM failures_: raw sensor values and rolling means, median, range, standard deviations, number of outliers beyond three standard deviations, upper and lower CUMESUM features were used.
- _Subway train door failures_: Counts of the events on the last day, counts of events over the previous 2 weeks and variance of counts of events of the previous 15 days were used to create lag features. Same counting was used for maintenance-related events.
- _Circuit breaker failures_: Failure counts were aggregated over last three years.

Another useful technique in PdM is to capture trend changes, spikes and level changes using algorithms that detect anomalies in data using anomaly detection algorithms.

#### *Tumbling aggregates*
For each labeled record of an asset, we pick a window of size "W-<sub>k</sub>" where k is the number or windows of size "W" that we want to create lag features for. "k" can be picked as a large number to capture long-term degradation patterns or a small number to capture short-term effects. We then use k _tumbling windows_ W-<sub>k</sub> , W-<sub>(k-1)</sub>, …, W-<sub>2</sub> , W-<sub>1</sub> to create aggregate features for the periods before the record date and time (see Figure 2).

![Figure 2. Tumbling aggregate features](./media/cortana-analytics-playbook-predictive-maintenance/tumbling-aggregate-features.png)

Figure 2. Tumbling aggregate features

As an example, for wind turbines, W=1 and k=3 months were used to create lag features for each of the last 3 months using top and bottom outliers.

### Static features

These are technical specifications of the equipment such as manufacture date, model number, location, etc. Static features usually become _categorical_ variables in the models. Examples for the circuit breaker use case included specifications on voltage, current, and power capacities, transformer types, power sources etc. For wheel failures, the type of tire wheels (alloy vs steel)are some examples of static features.

Other feature engineering steps include handling **missing values** and **normalization** of attribute values - an exhaustive discussion is out of the scope of this playbook.

> FURTHER READING: There are several books and papers on Feature Engineering. A sample of references:
> - Pyle, D. Data Preparation for Data Mining (The Morgan Kaufmann Series in Data Management Systems), 1999
> - Zheng, A., Casari, A. Feature Engineering for Machine Learning: Principles and Techniques for Data Scientists, O'Reilly, 2018.
> - Dong, G. Liu, H. (Editors), Feature Engineering for Machine Learning and Data Analytics (Chapman & Hall/CRC Data Mining and Knowledge Discovery Series), CRC Press, 2018.


At this stage of feature engineering, the training, test, validation and all new data that is provided for scoring should have data organized in the following schema (this example shows a day as the time unit).

| Asset ID | Time | Feature Columns | Label |
| ---- | ---- | --- | --- |
| A123 |Day 1 | . . . | . |
| A123 |Day 2 | . . . | . |
| ...  |...   | . . . | . |
| B234 |Day 1 | . . . | . |
| B234 |Day 2 | . . . | . |
| ...  |...   | . . . | . |

The last step in feature engineering is **labeling** of the target variable, which is dependent on the PdM algorithm/technique, which in turn, is decided based on the business problem and the nature of the availabel data. This is discussed in the next section.

## Modeling techniques for PdM

This section discusses the main modeling techniques for PdM problems, along with their specific label construction methods.

### Binary classification
Binary Classification is used to _predict the probability that a piece of equipment fails within a future time period_ - called the _future horizon period_, denoted by X. The future horizon period is determined by and based on business rules and the data at hand. Examples are:
- _minimum lead time_ required to replace components, deploy maintenance resources, perform  maintenance to preempt a problem that is likely to occur in that period.
- _minimum count_ of events that can happen before a problem can occur.

To use this technique, we identify two types of training examples - positive (which indicates a failure), and negative (which implies no failure), and define the labels as: label = 1 for positive type, and label = 0 for negative type. These labels are the value of the target variable and _categorical_. The goal is to find a model that identifies each new example as likely to fail or operate normally within the next X units of time.

#### Label construction
Labeling is done by taking X records prior to the failure of an asset and labeling them as "about to fail" (label = 1) while labeling all other records as "normal" (label =0). (see Figure 3). The goal is to find a model that identifies each new example as likely to fail or operate normally within the next X units of time.

![Figure 3. Labeling for binary classification](./media/cortana-analytics-playbook-predictive-maintenance/labelling-for-binary-classification.png)

Figure 3. Labeling for binary classification

For the use cases listed above:
- _Flight delays and cancellations_: X is chosen to be 1 day, to predict delays in the next 24 hours. All flights that are within 24 hours before failures were labeled as 1s.
- _ATM cash dispense failures_: Failure prediction could be failure in two areas: failure probability of a transaction in the next 10 minutes, and probability of failure in the next 100 notes dispensed. All transactions that happened within the last 10 minutes of the failure are labeled as 1 for the first model. And all notes dispensed within the last 100 notes of a failure were labeled as 1 for the second model.
- _Circuit breaker failures_: Probability that the next circuit breaker command fails in which case X is chosen to be one future command. For train door failures, the binary classification model was built to predict failures within the next 7 days. For wind turbine failures, X was chosen as 3 months.

### Regression for PdM
The goal for regression models for PdM is to _compute the remaining useful life (RUL) of an asset which is defined as the amount of time that the asset is operational before the next failure occurs_. Similar to binary classification, each example is a record that maps to a time unit "Y", or its multiple, for an asset that denotes the amount of time remaining for that example before the next failure. But unlike the categorial value for the target, the value for the target variable is a continuous number denoting the period of time remaining before the failure. We call this time period some multiple of Y.  

#### Label construction
Labels for the regression model are constructed by taking each record prior to the failure and labeling them by calculating how many units of time remain before the next failure. (See Figure 4)

![Figure 4. Labeling for regression](./media/cortana-analytics-playbook-predictive-maintenance/labelling-for-regression.png)

Figure 4. Labeling for regression

Since labeling is done in reference to a failure point, its calculation is not possible
without knowing how long the asset survived before failure. So in contrast to binary classification, assets without any failures in the data cannot be used for modeling. This issue
is best addressed by another statistical technique called [Survival Analysis](https://en.wikipedia.org/wiki/Survival_analysis). But this technique may not suitable for PdM use cases that involve time-varying data with frequent intervals - so it is not discussed in the playbook.

### Multi-class classification for PdM
Multi-class classification techniques can be used for PdM solutions in multiple ways:
- One technique is to predict _two future outcomes_. The first one could be to assign an asset to one of the multiple possible periods of time to give _a range of time to failure_ for each asset. The second one could identify the likelihood of failure in a future period due to _one of the multiple root causes_. This enables the maintenance crew to watch for symptoms and plan maintenance schedules.
- Another technique determines _the most likely root cause_ of a given a failure. This helps to prioritize or recommend the right set of maintenance actions to fix a failire. A ranked list of root causes and associated repair actions will help technicians prioritize their repair actions after failures.

#### Label construction
To address the question _"What is the probability that an asset fails in the next "aZ" units of time where "a" is the number of periods?"_, labeling is done by taking aZ records prior to the failure of an asset and labeling them using buckets of time (3Z, 2Z, Z) as their labels, and labeling all other records as "normal" (label = 0). In this method, the target variable holds categorical values - i.e. the label is categorical (See Figure 5).

![Figure 5. Labeling for multiclass classification for failure time prediction](./media/cortana-analytics-playbook-predictive-maintenance/labelling-for-multiclass-classification-for-failure-time-prediction.png)

Figure 5. Labeling for multiclass classification for failure time prediction

To address the question _"What is the probability that the asset fails in the next X units of time due to root cause/problem "RC<sub>i</sub>?"_ where "i" is the number of possible root causes, labeling is done by taking X records prior to the failure of an asset and labeling them as "about to fail due to problem P<sub>i</sub>" (label = RC<sub>i</sub>), and labeling all other records as "normal" (label = 0). In this method also, labels are categorical (See Figure 6).

![Figure 6. Labeling for multiclass classification for root cause prediction](./media/cortana-analytics-playbook-predictive-maintenance/labelling-for-multiclass-classification-for-root-cause-prediction.png)

Figure 6. Labeling for multiclass classification for root cause prediction

The model assigns a failure probability due to each RC<sub>i</sub> as well as the probability of no failure. These probabilities can be ordered by magnitude to allow prediction of the problems that are most likely to occur in the future.

To address the question _"What maintenance actions do you recommend after failures?", labeling does not require a future horizon to be picked. This is because the model is not predicting
failure in the future but it is just predicting the most likely root cause _once the failure has already happened_. 

## Modeling Techniques applies to PdM Use Cases

Given the knowledge of modeling techniques, let us see how they can be applied to the the [Sample PdM Use Cases](#Sample-PdM-Use-Cases):

| Use Case | Modeling Technique | Labelling notes |
|:---------|--------------------|-----------------|
|_Flight delay and cancellations_ | Multi-class classification model to predict the type of mechanical issue which results in a delay or cancellation of a flight in the next X hours. | X is chosen to be 1 day, to predict delays in the next 24 hours. All flights that are within 24 hours before failures were labeled as 1s.|
|_Aircraft engine parts failure_ | Multi-class classification model to predict the probability of a failure due to a certain component within the next N days | |
|_ATM Failure_ | Two separate binary classification models - the first one to predict transaction failures and the second to predict cash dispensing failures. Failure prediction could be failure in two areas: failure probability of a transaction in the next 10 minutes, and probability of failure in the next 100 notes dispensed. |All transactions that happened within the last 10 minutes of the failure are labeled as 1 for the first model. All notes dispensed within the last 100 notes of a failure were labeled as 1 for the second model.|
|_Wind turbine failure_ | |X was chosen as 3 months.|
|_Circuit breaker failures_ | Probability that the next circuit breaker command fails in which case X is chosen to be one future command.| |
|_Elevator door failures_|A multiclass logistic regression model to predict the cause of the failure given historical data on operating conditions. This model is then used to predict the most likely root causes after a failure has occurred.| |
|_Wheel failures_ | | |
|_Subway train door failures_ |For train door failures, the binary classification model was built to predict failures within the next 7 days. | |

## Training, validation and testing methods in PdM
[Team Data Science Process](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/overview) provides a full coverage of the model train-test-validate cycle. This section discusses aspects unique to PdM.

### Cross validation
The goal of [cross validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)) is to define a dataset to "test" the model in the training phase (i.e., the validation set), in order to limit problems like _overfitting_ and give an insight on how the model will generalize to an independent dataset (i.e., an unknown dataset, for instance from a real problem). The training and testing routine for PdM needs to take account the time varying aspects to better generalize on unseen future data.

Many machine learning algorithms depend on a number of hyperparameters that can change model performance significantly. The optimal values of these hyperparameters are not computed automatically when training the model, but should be specified by data scientist. There are several ways of finding good values of hyperparameters. The most common one is _k-fold cross-validation_ which splits the examples randomly into "k" folds. For each set of hyperparameters values, the learning algorithm is run k times. At each iteration, the examples in the current fold are used as a validation set, the rest of the examples are used as a training set. The algorithm trains over training examples and the performance metrics are computed over validation examples. At the end of this loop for each set of hyperparameter values, we compute average of the k performance metric values and choose hyperparameter values that have the best average performance.

In PdM problems, data is recorded as a time series of events that come from several data sources. These records can be ordered according to the time of labeling a record or an example. Hence, if we split the dataset randomly into training and validation set, _some of the training examples may be later in time than some of validation examples_. This results in estimating future performance of hyperparameter values based on the data that arrived before model was trained. These estimations might be overly optimistic, especially if time-series are not stationary and change their behavior over time. As a result, chosen hyperparameter values might be sub-optimal.

The recommended way of finding good values of hyperparameters is to split the examples into training and validation set _in a time-dependent way, such that all validation examples are later in time than all training examples_. Then, for each set of values of hyperparameters we can train the algorithm over training set, measure model’s performance over the same validation set and choose hyperparameter values that show the best performance. When time series data is not stationary and evolves over time, the hyperparameter values chosen by train/validation split lead to a better future model performance than with the values chosen randomly by cross-validation.

The final model can be generated by training a learning algorithm over entire training data using the best hyperparameter values that are found by using training/validation split or cross-validation.

### Testing for model performance
After building a model we need to estimate its future performance on new data. The simplest estimate could be the performance of the model over the training data. But this estimate is overly optimistic, because the model is tailored to the data that is used to estimate performance. A better estimate could be a performance metric of hyperparameter values computed over the validation set or an average performance metric computed from cross-validation. But for the same reasons as previously stated, these estimations are still overly optimistic. We need more
realistic approaches for measuring model performance.

One way is to split the data randomly into training, validation and test sets. The training and validation sets are used to select values of hyperparameters and train the model with them. The performance of the model is measured over the test set.

Another way which is relevant to PdM, is to split the examples into training, validation and test sets in a time-dependent way, such that all test examples are later in time than all training and
validation examples. After the split, model generation and performance measurement are done the same as described earlier.

When time-series are stationary and easy to predict both approaches generate similar estimations of future performance. But when time-series are non-stationary and/or hard to predict, the second approach will generate more realistic estimates of future performance than the first one.

### Time-dependent split
In this section we review best practices in implementing time-dependent split. We describe a time-dependent two-way split between training and test sets; the same logic can be applied
for time-dependent split for training and validation sets.

Suppose we have a stream of timestamped events such as measurements from various sensors. Features of training and test examples, as well as their labels, are defined over timeframes that contain multiple events. For example, for binary classification, as described in [Feature Engineering](#Feature-Engineering) and [Modeling Techniques](#Modeling-Techniques-applied-to-PdM-Use-Cases) sections, features are created based on past events and labels are created based on future events within "X" units of time in the future. Thus, the labeling timeframe of an example comes later then the timeframe of its features.

For time-dependent split, we pick a point in time at which we train a model with tuned hyperparameters by using historical data up to that point. To prevent leakage of future labels that are beyond the training cut-off into training data, we choose the latest timeframe to label
training examples to be X units before the training cut-off date. In Figure 7, each solid circle represents a row in the final feature data set for which the features and labels are computed according to the method described above. The figure shows the records that should go into training and testing sets when implementing time-dependent split for X=2 and W=3:

![Figure 7. Time-dependent split for binary classification](./media/cortana-analytics-playbook-predictive-maintenance/time-dependent-split-for-binary-classification.png)

Figure 7. Time-dependent split for binary classification

The green squares represent the records belonging to the time units that can be used for training. Each training example in the final feature table is generated by looking at past 3 periods for feature generation and 2 future periods for labeling before the training day cut-off. When any part of the 2 future periods for a given example is beyond the training cut-off, that example is excluded from the training dataset, since we assume that we do not have visibility beyond the training cut-off.

The black squares represent the records of the final labeled dataset that should not be used in the training data set, given the above constraint. These records won’t be used in testing data either since they are before the training cut-off. In addition, their labeling timeframes partially depend on the training timeframe, which is not ideal since training and test data should have completely separate labeling timeframes to prevent label information leakage.

This technique allows for overlap in the data used for feature generation between training and testing examples that are close to the training cut-off. Depending on data availability, an even more severe separation can be accomplished by not using any of the examples in the test set that are within W time units of the training cut-off.

Regression models used for predicting remaining useful life are more severely affected by the leakage problem and using a random split leads to extreme overfitting. Similarly, in regression problems, the split should be such that records belonging to assets with failures before training cut off should be used for the training set and assets that have failures after the cut-off should be used for testing set.

As a general method, another important best practice for splitting data for training and testing is to use a split by asset ID so that none of the assets that were used in training are used for testing since the idea of testing is to make sure that when a new asset is used to make predictions on, the model provides realistic results.

### Handling imbalanced data
In classification problems, if there are more examples of one class than of the others, the data is said to be imbalanced. Ideally, we would like to have enough representatives of each class in the training data to be able to differentiate between different classes. If one class is less
than 10% of the data, we can say that the data is imbalanced and we call the underrepresented dataset minority class. In many PdM problems, we can expect to find imbalanced datasets where one class is severely underrepresented compared to others for example by only constituting only 0.001% of the data points. Class imbalance is not unique to PdM - it is found in other domains including fraud detection, network intrusion where failures are usually rare occurrences in the lifetime of the assets which make up the minority class examples.

With class imbalance in data, performance of most standard learning algorithms is compromised as they aim to minimize the overall error rate. For example, for a data set with 99% negative class examples (i.e. no failures) and 1% positive class examples (i.e. failures), we can get 99% accuracy by simply labeling all instances as negative. However, this misclassifies all positive examples so the algorithm is not a useful one although the accuracy metric is very high. Consequently, conventional evaluation metrics such as _overall accuracy on error rate_, are not sufficient in case of imbalanced learning. Other metrics, such as _precision_, _recall_, _F1 scores_ and _cost adjusted ROC curves_ are used for evaluations in case of imbalanced datasets. These are discussed in the [Evaluation Metrics](#Evaluation-Metrics).

However, there are some methods that help remedy class imbalance problem. The two major ones are _sampling techniques_ and _cost sensitive learning_.

#### Sampling methods
The use of sampling methods in imbalanced learning consists of modification of the training dataset by some mechanisms in order to provide a balanced dataset. Sampling methods are not to be applied to the test set. Although there are several sampling techniques, most straight forward ones are _random oversampling_ and _under sampling_.

_Random oversampling_ involves selecting a random sample from minority class, replicating these examples and adding them to training data set. This increases the number of total examples in minority class and eventually balance the number of examples of different classes. One danger of oversampling is that multiple instances of certain examples can cause the classifier to become too specific leading to overfitting. This would result in high training accuracy but performance on the unseen testing data may be very poor.

Conversely, _random under sampling_ is selecting a random sample from majority class and removing those examples from training data set. However, removing examples from majority class may cause the classifier to miss important concepts pertaining to the majority class. _Hybrid sampling_ where minority class is oversampled and majority class is under sampled at the same time is another viable approach.

There are many other more sophisticated sampling techniques are available and effective sampling methods for class imbalance is a popular research area receiving constant attention and contributions from many channels. Use of different techniques to decide on the most effective ones is usually left to the data scientist to research and experiment and are highly dependent on the data properties.

#### Cost sensitive learning
In PdM, failures which constitute the minority class are of more interest than normal examples. So the performance of the algorithm on failures is usually the focus. This is commonly referred as unequal loss or asymmetric costs of misclassifying elements of different classes. In other words, incorrectly predicting a positive as negative can cost more than vice versa. The desired classifier should be able to give high prediction accuracy over the minority class, without severely compromising on the accuracy for the majority class.

There are several ways this can be achieved. By assigning a high cost to misclassification of the minority class, and trying to minimize the overall cost, the problem of unequal loses can be effectively dealt with. Some machine learning algorithms use this idea inherently such as _SVMs (Support Vector Machines)_ where cost of positive and negative examples can be incorporated during training time. Similarly, boosting methods are used and usually show good performance in case of imbalanced data such as boosted decision tree algorithms.

## Model Evaluation
As mentioned earlier, class imbalance causes poor performance as algorithms tend to classify majority class examples better in expense of minority class cases, and the total misclassification error is low when majority class is labeled correctly. This causes low
recall rates and becomes a larger problem when the cost of false alarms to the business is very high.

Accuracy is the most popular metric used for describing a classifier’s performance. However as explained above, accuracy is ineffective and does not reflect the real performance of a
classifier’s functionality as it is very sensitive to data distributions. Instead, for imbalanced learning problems, precision, recall and F1 scores should be the initial metrics to look at when evaluating PdM model performance.

In PdM, Precision metric relates to the rate of false alarms where lower precision rates correspond to higher false alarms. Recall rates denote how many of the failures in the test set were correctly identified by the model. Higher recall rates mean the model is successful in catching the true failures. F1 score considers both precision and recall rates with best value being 1 and worst being 0.

For binary classification, _decile tables_ and _lift charts_ are very informative when evaluating performance. They focus only on the positive class (failures) and provide a more complex picture of the algorithm performance than what is seen by looking at just a fixed operating point on the _ROC (Receiver Operating Characteristic) curve_.

Decile tables are obtained by ordering the test examples according to their predicted probabilities of failures computed by the model before thresholding to decide on the final label. The ordered samples are then grouped in deciles (i.e. the 10% samples with largest probability and
then 20%, 30% and so on). By computing the ratio between true positive rate of each decile and its random baseline (i.e. 0.1, 0.2 ..) one can estimate how the algorithm performance changes at each decile.

Lift charts are used to plot decile values by plotting decile true positive rate versus random true positive rate pairs for all deciles. Usually, the first deciles are the focus of the results since here we see the largest gains. First deciles can also be seen as representative for "at
risk" when used for PdM.

## **Solution Templates for PdM**

In this final section of this playbook, we present a list of solution templates that are built based on all the principles stated above. You can deploy these solution templates to your Azure subscription in a few hours, understand how they work, and then use/adapt them to build your PdM solutions on Azure.

The common aspect of all solution templates is that they are all implemented using Azure Data, AI and IoT technologies. They are either located in the [Azure AI Gallery](http://gallery.azure.ai), or managed in the Microsoft Azure GitHub (https://github.com/Azure).

> **HOW YOU CAN HELP**: There are several articles and solution templates on PdM available as
> Bing or Google Search results. Most are functionally complete, a few represent the state of the
> art Azure ML v2.0 preview, but a few of the templates and articles are incomplete.
> You can help in two ways: report any issues with these solution templates to
> ciqsoncall@microsoft.com. Also, contact us if you are interested in updating these solution
> templates to the latest Azure technologies, or want to contribute new PdM solution
> templates on Azure.

| Solution Template Title | Description |
|:------------------------|-------------|
|[Azure Predictive Maintenance Machine Learning Sample](https://github.com/Azure/MachineLearningSamples-PredictiveMaintenance) |PdM sample that demonstrates use of latest Azure ML on DSVM on sample CSV data. Ideal for beginners to PdM.|
|[Azure Predictive Maintenance Solution Template](https://github.com/Azure/AI-PredictiveMaintenance) | An end to end implementation of a 
|[Azure AI Toolkit for IoT Edge](https://github.com/Azure/ai-toolkit-iot-edge) | AI in the IoT edge using TensorFlow; toolkit packages deep learning models in Azure IoT Edge-compatible Docker containers and expose those models as REST APIs.
| [Azure Predictive Maintenance for Aerospace](https://gallery.azure.ai/Solution/Predictive-Maintenance-for-Aerospace-1) | One of the early PdM solution templates based on Azure ML v1.0 for aircraft maintenance. This playbook originated from this project |
| [Azure IoT Predictive Maintenance](https://github.com/Azure/azure-iot-predictive-maintenance) | Azure IoT Suite PCS - Preconfigured Solution. Aircraft maintenance PdM template with IoT Suite |
|[Predictive Maintenance Modeling Guide in R](https://gallery.azure.ai/Notebook/Predictive-Maintenance-Modelling-Guide-R-Notebook-1) | PdM modeling guide in Azure ML v1.0 |
| More ... | |