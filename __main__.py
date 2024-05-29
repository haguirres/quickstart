"""An Azure RM Python Pulumi program"""

import pulumi
from networking import virtual_network, network_security_group, subnet
from resources import resource_group

# Common variables
location = "mexicocentral"
tags = {
    "environment": "dev",
    "owner": "HEAS"
}

# Resource group variables
resource_group_name = "rg-demo-pulumi-mc"

# Virtual network variables
vnet_name = "demo_virtual_network"
address_space = ["10.0.0.0/16"]
dns_servers = []
flow_timeout_in_minutes = 4
enable_ddos_protection = False
encryption = {"enabled": False, "enforcement": None}
enable_vm_protection = False
subnets = [
    {
        "name": "BastionSubnet",
        "addressPrefix": "10.0.1.0/24",
        "nsg": {
            "name": "BastionNSG",
            "security_rules": [
                {
                    "name": "AllowSSH",
                    "priority": 1000,
                    "direction": "Inbound",
                    "access": "Allow",
                    "protocol": "Tcp",
                    "source_port_range": "*",
                    "destination_port_range": "22",
                    "source_address_prefix": "*",
                    "destination_address_prefix": "*"
                },
                {
                    "name": "AllowHTTPS",
                    "priority": 1100,
                    "direction": "Inbound",
                    "access": "Allow",
                    "protocol": "Tcp",
                    "source_port_range": "*",
                    "destination_port_range": "43",
                    "source_address_prefix": "*",
                    "destination_address_prefix": "*"
                }
            ]
        }
    },
    {
        "name": "AppGatewaySubnet",
        "addressPrefix": "10.0.2.0/24",
        "nsg": {
            "name": "AppGatewayNSG",
            "security_rules": [
                {
                    "name": "AllowHTTPS",
                    "priority": 1100,
                    "direction": "Inbound",
                    "access": "Allow",
                    "protocol": "Tcp",
                    "source_port_range": "*",
                    "destination_port_range": "43",
                    "source_address_prefix": "*",
                    "destination_address_prefix": "*"
                }
            ]
        }
    },
    {
        "name": "PrivateSubnet",
        "addressPrefix": "10.0.3.0/24",
        "nsg": {
            "name": "PrivateNSG",
            "security_rules": [
                {
                    "name": "AllowSSH",
                    "priority": 1000,
                    "direction": "Inbound",
                    "access": "Allow",
                    "protocol": "Tcp",
                    "source_port_range": "*",
                    "destination_port_range": "22",
                    "source_address_prefix": "*",
                    "destination_address_prefix": "*"
                },
                {
                    "name": "AllowHTTPS",
                    "priority": 1100,
                    "direction": "Inbound",
                    "access": "Allow",
                    "protocol": "Tcp",
                    "source_port_range": "*",
                    "destination_port_range": "43",
                    "source_address_prefix": "*",
                    "destination_address_prefix": "*"
                },
                {
                    "name": "AllowRDP",
                    "priority": 1200,
                    "direction": "Inbound",
                    "access": "Allow",
                    "protocol": "Tcp",
                    "source_port_range": "*",
                    "destination_port_range": "3389",
                    "source_address_prefix": "*",
                    "destination_address_prefix": "*"
                },
                {
                    "name": "AllowSQL",
                    "priority": 1300,
                    "direction": "Inbound",
                    "access": "Allow",
                    "protocol": "Tcp",
                    "source_port_range": "*",
                    "destination_port_range": "1433",
                    "source_address_prefix": "*",
                    "destination_address_prefix": "*"
                }
            ]
        }
    },
    {
        "name": "PublicSubnet",
        "addressPrefix": "10.0.4.0/24",
        "nsg": {
            "name": "PublicNSG",
            "security_rules": [
                {
                    "name": "AllowSSH",
                    "priority": 1000,
                    "direction": "Inbound",
                    "access": "Allow",
                    "protocol": "Tcp",
                    "source_port_range": "*",
                    "destination_port_range": "22",
                    "source_address_prefix": "*",
                    "destination_address_prefix": "*"
                },
                {
                    "name": "AllowHTTPS",
                    "priority": 1100,
                    "direction": "Inbound",
                    "access": "Allow",
                    "protocol": "Tcp",
                    "source_port_range": "*",
                    "destination_port_range": "43",
                    "source_address_prefix": "*",
                    "destination_address_prefix": "*"
                },
                {
                    "name": "AllowRDP",
                    "priority": 1200,
                    "direction": "Inbound",
                    "access": "Allow",
                    "protocol": "Tcp",
                    "source_port_range": "*",
                    "destination_port_range": "3389",
                    "source_address_prefix": "*",
                    "destination_address_prefix": "*"
                },
                {
                    "name": "AllowSQL",
                    "priority": 1300,
                    "direction": "Inbound",
                    "access": "Allow",
                    "protocol": "Tcp",
                    "source_port_range": "*",
                    "destination_port_range": "1433",
                    "source_address_prefix": "*",
                    "destination_address_prefix": "*"
                }
            ]
        }
    }
]

# Resource creation
resource_group_instance = resource_group.create_resource_group(
    resource_group_name,
    location,
    tags)

# Virtual Network creation
virtual_network_instance = virtual_network.create_virtual_network(
    resource_group_instance.name, location, tags, vnet_name, address_space, dns_servers, flow_timeout_in_minutes, encryption, enable_vm_protection, enable_ddos_protection)

# Create NSGs and subnets
subnet_instances = []
nsg_instances = []

for subnet_config in subnets:
    nsg_instance = network_security_group.create_network_security_group(
        resource_group_name=resource_group_instance.name,
        nsg_name=subnet_config["nsg"]["name"],
        location=location,
        tags=tags,
        security_rules=subnet_config["nsg"]["security_rules"]
    )
    nsg_instances.append(nsg_instance)

    subnet_instace = subnet.create_subnet(
        vnet_name,
        resource_group_instance.name,
        subnet_config["name"],
        subnet_config["addressPrefix"],
        nsg_instance
    )
    subnet_instances.append(subnet_instace)

# Export IDs
pulumi.export("RG_ID", resource_group_instance.id)
pulumi.export("VNET_ID", virtual_network_instance.id)
pulumi.export("NSG_IDs", [nsg.id for nsg in nsg_instances])
pulumi.export("SUBNET_IDs", [subnet.id for subnet in subnet_instances])
