# Objectives
# Concepts and fundamentals
## Source control
[Visual Studio Team Services (VSTS)](https://docs.microsoft.com/en-us/vsts/index?view=vsts) provides a [new user guide](https://docs.microsoft.com/en-us/vsts/user-guide/?view=vsts) to get started with VSTS and Git.
## Infrastructure as code (IaC)
This solution template includes a set of Azure Resource Manager (ARM) templates to provision Azure resources for the PdM demo scenario.  As you modify and extend the solution to meet your production needs, modeling your own infrastructure as code will avoid environment drift between your testing, qualification, and production environments.  You can leverage [Microsoft's best practices for infrastructure as code](https://docs.microsoft.com/en-us/azure/devops/what-is-infrastructure-as-code).
## Environments - Dev-test and production
In order to reduce the risk of promoting code into production, the best practices guidance from Azure is to create isolated environments to enable development, quality assurance (QA), and production.  You can leverage the reference architecture guides for [Platform as a Service (PaaS)](https://azure.microsoft.com/en-us/solutions/architecture/dev-test-paas/) and [microservices](https://azure.microsoft.com/en-us/solutions/architecture/dev-test-microservice/).
## Continuous integration and continuous delivery - CICD
Replacing manual gates between environments with automation accelerates delivery of changes to production.  You can leverage Microsoft's architecture guides with [CICD for webapps](https://azure.microsoft.com/en-us/solutions/architecture/vsts-continuous-integration-and-continuous-deployment-for-azure-web-apps/) and [CICD for containers](https://azure.microsoft.com/en-us/solutions/architecture/cicd-for-containers/).
## Application monitoring
[Azure Application Insights](https://docs.microsoft.com/en-us/azure/application-insights/) is the Microsoft Azure best practice for monitoring your application performance.  [Azure Monitor](https://docs.microsoft.com/en-us/azure/monitoring/) is the Microsoft Azure best practice for monitoring your application infrastructure.
## Prediction monitoring
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
