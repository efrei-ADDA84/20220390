data "azurerm_virtual_network" "network_tp4" {
  name                = var.network_tp4
  resource_group_name = var.resource_group_name
}


data "azurerm_subnet" "subnet_tp4" {
  name                = var.subnet_tp4
  virtual_network_name = var.network_tp4
  resource_group_name = var.resource_group_name
}