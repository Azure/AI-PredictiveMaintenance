Param(
  [string]$storageAccountName,
  [string]$storageAccountKey
)
$progressPreference = "silentlyContinue"
$containerName = "telemetry"
$fileshareName = "azureml-share"
$ErrorActionPreference = "Stop"
$ctx = New-AzureStorageContext -StorageAccountName $storageAccountName -StorageAccountKey $storageAccountKey
New-Item -Path "D:\home\site\wwwroot" -Name "SetupLog.txt" -ItemType "file" 

$success = $false
$i =0
while((!$success))
{
  try
  {
    New-AzureStorageContainer -Name $containerName -Context $ctx -Permission Off
    Get-AzureStorageContainer -Name $containerName -Context $ctx
    $success = $true
  }
  catch{
    $message = 'Creating telemetry container failed : ' + $_.Exception.Message
    Add-Content -Path "D:\home\site\wwwroot\SetupLog.txt" -Value $message 
    if($i -gt 4)
    {
      throw
    }
    $i =$i +1
    Start-Sleep -s 15
  }
}


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
    $message = 'Creating azuremlshare file share failed : ' + $_.Exception.Message
    Add-Content -Path "D:\home\site\wwwroot\SetupLog.txt" -Value $message 
    if($i -gt 4)
    {
      throw
    }
    $i =$i +1
    Start-Sleep -s 15
  }
}

$fileshareName = "azureml-project"
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
    $message = 'Creating azuremlshare file share failed : ' + $_.Exception.Message
    Add-Content -Path "D:\home\site\wwwroot\SetupLog.txt" -Value $message 
    if($i -gt 4)
    {
      throw
    }
    $i =$i +1
    Start-Sleep -s 15
  }
}
