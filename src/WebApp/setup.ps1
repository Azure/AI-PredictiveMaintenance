Param(
  [string]$storageAccountName,
  [string]$storageAccountKey
)

$ctx = New-AzureStorageContext -StorageAccountName $storageAccountName -StorageAccountKey $storageAccountKey

$containerName = "telemetry"
$fileshareName = "azureml-share"
New-AzureStorageContainer -Name $containerName -Context $ctx -Permission Off

New-AzureStorageShare -Name $fileshareName -Context $ctx
