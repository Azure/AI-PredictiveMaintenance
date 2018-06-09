#!/bin/bash
wget -O spark-logo.png https://spark.apache.org/images/spark-logo-trademark.png
wget -O kafka-logo.png https://svn.apache.org/repos/asf/kafka/site/logos/kafka-logo-no-text.png
wget -O event-hub.svg https://worldvectorlogo.com/download/azure-event-hub.svg
wget -O iot-hub.svg "https://azure.microsoft.com/svghandler/iot-hub/?width=600&amp;height=600"
wget -O databricks.svg "https://azure.microsoft.com/svghandler/databricks?width=600&height=600"
wget -O table-storage.svg "https://docs.microsoft.com/en-us/azure/media/index/storage.svg"
wget -O stream-analytics.svg "https://azure.microsoft.com/svghandler/stream-analytics?width=600&height=600"
wget -O sql-database.svg "https://azure.microsoft.com/svghandler/sql-database?width=600&height=600"
wget -O cosmos-db.svg "https://azure.microsoft.com/svghandler/cosmos-db?width=600&height=600"
wget -O webjob.png https://developersde.blob.core.windows.net/usercontent/2018/4/15734_webjobs.png
wget -O aks.png https://stephanefrechette.com/wp-content/uploads/2018/04/Azure-Container-Service_COLOR-300x300.png
wget -O dashboard.png https://www.freeiconspng.com/uploads/dashboard-icon-3.png
wget -O blob-storage.png https://azureautomation950740325.files.wordpress.com/2018/02/azure-storage-blob.png
wget -O python-logo.png https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/2000px-Python-logo-notext.svg.png
wget -O dsvm.svg "https://azure.microsoft.com/svghandler/virtual-machines-data-science-virtual-machines/?width=600&height=600"
wget -O databricks.png "https://databricks.com/wp-content/themes/databricks/assets/images/header_logo.png"
wget -O file-storage.png "https://ievgensaxblog.files.wordpress.com/2017/07/azure-storage-files.png"
wget -O aml-workbench.svg "http://azureml.azureedge.net/content/apphome/media/AML-Logo.svg"
wget -O model.png "https://vc4prod.blob.core.windows.net/catalog/Recommendations/Machine-Learning.png"
wget -O jupyter.png "http://jupyter.org/assets/try/jupyter.png"

convert -density 300 event-hub.svg event-hub.png
convert -density 300 iot-hub.svg iot-hub.png
convert -density 300 databricks.svg databricks.png
convert -density 300 table-storage.svg table-storage.png
convert -density 300 stream-analytics.svg stream-analytics.png
convert -density 300 sql-database.svg sql-database.png
convert -density 300 cosmos-db.svg cosmos-db.png
convert -density 300 dsvm.svg dsvm.png
convert -density 300 aml-workbench.svg aml-workbench.png
