# Objectives
# Concepts and fundamentals
## Source control
Git, GitHub, VSTS - TODO
## Infrastructure as code (IaC)
This solution template includes a set of Azure Resource Manager (ARM) templates to provision Azure resources for the PdM demo scenario.  As you modify and extend the solution to meet your production needs, modeling your infrastructure as code will enable you to avoid environment drift between your testing, qualification, and production environments.  Familiarize yourself with [Microsoft's best practices for infrastructure as code](https://docs.microsoft.com/en-us/azure/devops/what-is-infrastructure-as-code).
## Environments - Dev-test and production
In order to reduce the risk of promoting code into production, the best practices guidance from Azure is to create isolated environments to enable development, quality assurance (QA), and production.  You can explore the reference architecture guides for [Platform as a Service (PaaS)](https://azure.microsoft.com/en-us/solutions/architecture/dev-test-paas/) and [microservices](https://azure.microsoft.com/en-us/solutions/architecture/dev-test-microservice/).
## Continuous integration and continuous delivery - CICD
# Modeling + retraining
## Device manufacturer device telemetry guidance, parts maintenance schedule
## Long term storage of maintenance records, security
## Small scale modeling on the DSVM
## Large scale modeling featurization - Infrastructure guidance, on-demand cluster provisioning, data pump, velocity monitoring
## Large scale model training - Infrastructure guidance, on-demand cluster provisioning, data pump, velocity monitoring
## Model accuracy
## Model management
# Scoring pipeline
## Real time data ingress: IoT hub, scale, security
## Long term storage of live data - blob storage (archive), table storage, security
## Real time featurization - Infrastructure guidance, scale, security, CICD, monitoring, logging, alerting, defect root cause
## Storing featurized data - featurizer version, cluster id, node id, long term storage, security, auditability
## Real time scoring - Infrastructure guidance (ACI, AKS), scale, security, CICD, monitoring, logging, alerting, defect root cause
## Storing scored data - scorer version, cluster id, node id, long term storage, security, auditability
## Presentation of predictions
## Consumption of predictions
