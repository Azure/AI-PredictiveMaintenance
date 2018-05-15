# Azure AI Learning Path for Predictive Maintenance
_Contributors: [Anish Mohan](https://github.com/animohan), [Ramkumar Krishnan](https://github.com/ramkumarkrishnan)_

Predictive maintenance (PdM) solutions helps businesses make use of their assets effectively, which translates to savings in operational costs.

The data science described in [Azure AI Guide for Predictive Maintenance Solutions](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/cortana-analytics-playbook-predictive-maintenance.md) is based on foundational concepts from mathematics, statistics, information theory, and cognitive science. The processing to enable this data science is based on distributed compute and storage systems. This document provides a learning path for a reader interested in learning these foundational concepts.

## 'Classical' machine learning techniques for PdM

This section provides the learning path to understand 'classical' supervised learning algorithms for classification and regression.

- Classifiers predict a _categorical_ output that could be binary (Failure=Yes/No) or multi-class (Failure_type=Type01/Type02/Type03)
- Regression algorithms predict a _numerical_ output. Examples are number of days to failure, temperature/pressure/vibration frequency at which failure could occur, and so on.

The key algorithms in this space are:
- Basic Decision Trees
- Classification and Regression Trees ([CART, Leo Breiman et al.](https://www.amazon.com/Classification-Regression-Wadsworth-Statistics-Probability/dp/0412048418))
- Tree pruning methodologies
- Accuracy measure for Decision trees
- Bagged Trees (Bagging)
- Random Forest

### Learning Path for classical ML techniques

| # | Concept            | Description | Modality | Time |
|:--|------------------|-------------|----------|------|
| 1 | [Basic Statistics](https://www.edx.org/course/essential-mathematics-for-artificial-intelligence-dat256x) | This course covers the key mathematical concepts required to understanding and building machine learning models. Key sections required for the PdM learning path are (1) Statistics Fundamentals and (2) Probability | Course | 2 hours |
| 2 | [Hypothesis Testing and Handling Data](https://www.edx.org/course/data-science-essentials-microsoft-dat203-1x-6) | The next step is to understand concepts of hypothesis testing and basic data manipulation methods. Key sections required for the PdM learning path: (1)	Simulation and Hypothesis Testing (2) Exploring and Visualizing Data (3) Data Cleansing and Manipulation | Course | 5 hours |
| 3 | [Data preparation and Feature engineering](https://www.edx.org/course/programming-python-data-science-microsoft-dat210x-6) | The next set of modules is from a _Python for Programming_ course. It covers the key aspects of working with various kinds of data, data manipulation, and managing/building features. Key sections required for this learning path: (1)	Data and Features (2) Data Transformation | Course | 2 hours |
| 4 | [Machine Learning Algorithms](https://www.edx.org/course/principles-machine-learning-microsoft-dat203-2x-6) | After covering the basic data and feature management, next step is look at two key categories of Machine Learning algorithms. This course also introduces the concept of validating statistical and machine learning models. This course covers the theoretical underpinning of machine learning concepts and explains the key machine learning algorithms. The key sections required for this learning path: (1) Classification problems (2) Regression problems (3) Model management | Course | 4 hours |
| 5 | [Introduction to PySpark](https://www.datacamp.com/courses/introduction-to-pyspark) | This course introduces PySpark and shows how to build a machine learning pipeline using PySpark | Course | 4 hours |
| 6 | [Basic Decision Trees](https://docs.microsoft.com/en-us/sql/analysis-services/data-mining/microsoft-decision-trees-algorithm) | The above sections are a good preparation to deep-dive into the easiest to understand, transparent, powerful, and elegant classification algorithms - Decision Trees. This document provides a good overview of Decision trees. | Document | 1 hour |
| 7 | [Implementing Decision Trees](https://www.edx.org/course/programming-python-data-science-microsoft-dat210x-6) | This course covers the basic concepts related to Decision trees and its variants. This content leads into an introduction to Random Forests. The key sections required for this learning path: Data Modeling-Decision Trees. | Course | 3 hours |
| 8 | [Building and Deploying a Decision Tree/Random Forest model using PySpark](https://gallery.azure.ai/Tutorial/Predictive-Maintenance-using-PySpark) | This document explains the methodology to implement a Random Forest Model for a Predictive Maintenance scenario using PySpark | Document | 2 hours |

## Deep Learning techniques for PdM

Classical ML techniques require extensive feature engineering to be able to build effective models. In contrast, certain deep learning techniques like Long Short Term Memory (LSTM) networks are adept at learning from sequences. Applications like PdM that use time series data can benefit from the algorithm's ability to look back for longer periods of time to detect failure patterns. For more information, see [Deep Learning for Predictive Maintenance](https://azure.microsoft.com/en-us/blog/deep-learning-for-predictive-maintenance/).

Traditional PdM models require feature engineering. Choice of features depends on the problem and available data. Data varies widely from one scenario to the other. Consequently, reuse of models becomes difficult. Deep learning techniques may help automatically extract the right features from the data. But with DNNs, the developer has to define the topology with the optimal number of layers,  nodes, and hyperparameters.

The key concepts and techniques in this space are:
- Perceptron Model
- Neural Network
- Gradient Descent and Optimization Techniques
- Deep Neural Network
- Recurrent Neural Network
- Long-Short Term Memory

### Learning Path for Deep Learning algorithms

| # | Concept          | Description | Modality | Time |
|:--|------------------|-------------|----------|------|
| 1 | [Basic Statistics](https://www.edx.org/course/essential-mathematics-for-artificial-intelligence-dat256x) | This course covers the key mathematical concepts required to understanding and building machine learning models. Key sections required for the PdM learning path are (1) Statistics Fundamentals and (2) Probability | Course | 2 hours |
| 2 | [Hypothesis Testing and Handling Data](https://www.edx.org/course/data-science-essentials-microsoft-dat203-1x-6) | The next step is to understand concepts of hypothesis testing and basic data manipulation methods. Key sections required for the PdM learning path: (1)	Simulation and Hypothesis Testing (2) Exploring and Visualizing Data (3) Data Cleansing and Manipulation | Course | 5 hours |
| 3 | [Data preparation and Feature engineering](https://www.edx.org/course/programming-python-data-science-microsoft-dat210x-6) | The next set of modules is from a _Python for Programming_ course. It covers the key aspects of working with various kinds of data, data manipulation, and managing/building features. Key sections required for this learning path: (1)	Data and Features (2) Data Transformation | Course | 2 hours |
| 4 | [Deep Learning Explained](https://www.edx.org/course/deep-learning-explained-microsoft-dat236x-0) | This course provides an introduction to Deep Neural Networks, and demonstrates the implementation of a DNN using Microsoft Cognitive Tool Kit. Key sections required for this learning path are: (1) Overview (2) Multi-class classification (3) Multi-Layer Perceptron (Deep Neural Networks) | Course | 10 hours |
| 5 | [Deep Learning Explained](https://www.edx.org/course/deep-learning-explained-microsoft-dat236x-0) | This section introduces the Recurrent Neural Network and the LSTM network.| Course | 10 hours |
| 6 | [LSTM Networks Explained](https://github.com/Azure/lstms_for_predictive_maintenance/blob/master/Deep-Learning-Basics-for-Predictive-Maintenance.ipynb)) | This notebook explains the process to build an LSTM Deep Neural Network for predictive maintenance problems.| Document | 2 hours |
