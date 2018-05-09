Param(
  [string]$storageAccountName,
  [string]$storageAccountKey
)
$progressPreference = "silentlyContinue"
$containerName = "telemetry"
$fileshareName = "azureml-share"
$ErrorActionPreference = "Stop"
$ctx = New-AzureStorageContext -StorageAccountName $storageAccountName -StorageAccountKey $storageAccountKey

New-AzureStorageContainer -Name $containerName -Context $ctx -Permission Off

$success = $false
$i =0
while((!$success))
{
  try
  {
    New-AzureStorageShare -Name $fileshareName -Context $ctx
    Get-AzureStorageFile -ShareName $fileshareName -Context $ctx
    $success = $true
  }
  catch{
    if($i -gt 4)
    {
      throw
    }
    $i =$i +1
    Start-Sleep -s 15
  }
}
