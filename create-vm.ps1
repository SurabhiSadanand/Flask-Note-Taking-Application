# Connect to Azure account using a managed identity (used in Automation Accounts or Azure VMs)

# Authenticate using Managed Identity
$null = Connect-AzAccount -Identity

# Define variables for the resource group creation
$resourceGroupName = "MyRG"
$location = "EastUS"

# Check if the resource group exists
$resourceGroup = Get-AzResourceGroup -Name $resourceGroupName -ErrorAction SilentlyContinue

if (-not $resourceGroup) {
    # Create the resource group if it doesn't exist
    New-AzResourceGroup -Name $resourceGroupName -Location $location
    Write-Output "Resource group '$resourceGroupName' created in location '$location'."
} else {
    Write-Output "Resource group '$resourceGroupName' already exists."
}

