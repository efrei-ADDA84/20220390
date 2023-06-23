output "virtual_network_id" {
  value = data.azurerm_virtual_network.network_tp4.id
}

output "subnet_id" {
  value = data.azurerm_subnet.subnet_tp4.id
}