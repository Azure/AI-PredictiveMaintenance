# Model Creation and Operationalization

In simple terms, this solution template shows how to _train_ a _classification_ model,
based on a _training dataset_ from device sensor readings, maintenance and error logs,
_test_ the model for its accuracy using a _test dataset_, and _score_ newly arriving
device data using the model, and getting a _prediction_ on whether a device will fail
in the next N days (N=7 in this example), and if yes, with the type of failure.

The logical input, consisting of all _predictor variables_ would be several rows like this.

| Timestamp | machine | pressure | speed | ... | model | age | ... | failure | error |
|-----------|---------|----------|-------|-----|-------|-----|-----|-----|-----|
|2016-01-01 12:00:00 | m27 | 162.37 | 445.71 | ... | model3 | 9 | ... | 0.0 | 0.3 |

This input would be sampled into a candidate data set of a few 10Ks of rows, split
40-30-30 between training, test, and validation data sets. Then the model would be
trained and for each logical row of input, a row of scored output, like this:

| machine | ... _attributes_ ... | error | <span style="color:green">_will_fail_ | <span style="color:green">_failure_type_ |
|-----------|---------|-----|-------|-----------|
| m27 | ... | 0.3 | yes | F034 | 0.85034 |

The feature engineering, model creation, model validation/testing, and model operationalization are described in the documentation sections of the following Jupyter notebooks:

- [FeatureEngineering.ipynb](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/src/AML/Notebooks/FeatureEngineering.ipynb)
- [ModelTraining.ipynb](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/src/AML/Notebooks/ModelTraining.ipynb)
- [Operationalization.ipynb](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/src/AML/Notebooks/Operationalization.ipynb)

 These notebooks can be executed in their respective cluster environments, as explained in [Architecture](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/Architecture.md).  To avoid duplication, the reader is referred to the documentation in these notebooks.
