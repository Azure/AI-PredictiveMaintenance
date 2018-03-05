$ctx = New-AzureStorageContext -StorageAccountName $Env:STORAGE_ACCOUNT_NAME -StorageAccountKey $Env:STORAGE_ACCOUNT_KEY

$containerName = "telemetry"
New-AzureStorageContainer -Name $containerName -Context $ctx -Permission Off

$tableName = "equipment"
$table = Get-AzureStorageTable -name $tableName -Context $ctx -ErrorAction Ignore
if (-not $table) { 
    New-AzureStorageTable -Name $tableName -Context $ctx
}
