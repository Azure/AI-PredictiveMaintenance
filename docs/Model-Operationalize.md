# Model Operationalization

This section describes how to deploy models for the different use cases. The description for all use cases are placed together to help compare/contrast the different methods to operationalize models.

## Use Case 1 - Failure detection with real-time data
This is a new use case that makes use of data from a synthetic data generator and creates output results that show whether a failure or success happened for individual cases.

The code for this solution is located at
$GITHUBROOT\src\Notebooks\Solution_1\Operationalization.ipynb

## Use Case 2 - Prediction of failure over the next N time units
This use case is directly derived from the [Machine Learning sample for Predictive Maintenance](https://github.com/Azure/MachineLearningSamples-PredictiveMaintenance). The few changes from the original are:
- this sample runs in the local DSVM
- consequently, there will be changes in the source to accommodate directory structures and to pull in the right files into the local Jupyter environment.

The code for this solution is located at
$GITHUBROOT\src\Notebooks\Solution_2\Operationalization.ipynb
