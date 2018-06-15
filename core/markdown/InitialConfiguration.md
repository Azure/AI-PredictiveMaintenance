## Linux Data Science Virtual Machine (DSVM)
This solution creates and configures an instance of the *DSVM* to serve as the default modeling workstation. Please provide VM's size and admin user's credentials below.

## Azure Databricks

To demonstrate a production data pipeline with online feature engineering and scoring, we require programmatic access to an *Azure Databricks* workspace.

As an option, we also provide integration with *Azure Databricks* for performing interactive modeling. This can be useful in scenarios dealing with large input raw data.

If you already have a *Databricks* workspace and would like the solution to use it, please select "No" as your answer to "Create Databricks workspace?" below. Otherwise, a new workspace will be created.

In the following configuration screen, we will ask you to provide a *Databricks* personal access token. It will be used for creating a cluster to run the solution's online featurization job (Spark Structured Streaming) and to upload sample notebooks for ML modeling.
