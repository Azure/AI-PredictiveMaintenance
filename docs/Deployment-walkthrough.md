# Deployment Walk-through

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

#### Please send your questions, feedback, comments to ciqsoncall@microsoft.com

## Resource Consumption

**Estimated Daily Cost:** $20 per day

List of Azure services in this solution template deployment:

![Resources](https://github.com/Azure/AI-PredictiveMaintenance/blob/master/docs/img/Resources.png)

## Advanced Topics

### Data Science behind the Failure Prediction solution

### Problem Statement
The problem here is to predict the failure of a device, indicating the type of failure, along with the probability (chance) of its occurrence, over the next N days, given a set of _predictor variables_ such as temperature, pressure, etc over time.

Stated in modeling terms, this is a _multi-class classification_ problem that _classifies_ the target variable _failure_ to one of the different failure types, called _classes_. From the [recommended set of algorithms](https://docs.microsoft.com/en-us/azure/machine-learning/studio/algorithm-cheat-sheet), we choose the one that affords accuracy and speed of model creation, namely, _multi-class decision forest_.

### Data Preparation

### Model Creation

### Model Testing

### Model Validation

### Architecture of the Failure Prediction solution

## Related Work
There is rich content on predictive maintenance in both Microsoft and external websites. But most of them are experiments or tutorials to prove just one small aspect of the end to end solution, which can frustrate or confuse a user or solution architect trying to quickly bootstrap a Microsoft solution on proven, state of the art products. This template will be extended to provide a means for these contributor to upgrade and roll in their solutions into this template, and retire their old templates.