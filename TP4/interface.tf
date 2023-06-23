#Create Public IP adress
resource "azurerm_public_ip" "terraform_public_ip" {
  name                = "terraform_public_ip"
  resource_group_name = var.resource_group_name
  location            = var.location
  allocation_method   = "Static"
}


#Create the network interface
resource "azurerm_network_interface" "terraform-network_interface" {
  name                = "terraform-interface"
  location            = var.location
  resource_group_name = var.resource_group_name

  ip_configuration {
    name                          = "testconfiguration1"
    subnet_id                     = data.azurerm_subnet.subnet_tp4.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.terraform_public_ip.id
  }
}