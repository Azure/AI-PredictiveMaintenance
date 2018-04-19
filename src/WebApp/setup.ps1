Param(
  [string]$storageAccountName,
  [string]$storageAccountKey
)

$ctx = New-AzureStorageContext -StorageAccountName $storageAccountName -StorageAccountKey $storageAccountKey

$containerName = "telemetry"
New-AzureStorageContainer -Name $containerName -Context $ctx -Permission Off
