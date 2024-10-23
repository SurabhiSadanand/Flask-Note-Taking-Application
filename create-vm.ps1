$cred = Get-Credential
New-AzVm -ResourceGroupName "myResourceGroup" -Name "myVM" -Location "CanadaCentral" -Image "Canonical:UbuntuServer:18.04-LTS:18.04.202401161" -Credential $cred

