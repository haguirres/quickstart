import pulumi
from pulumi_azure_native import network


def create_nat_gateway(resource_group_name, nat_gateway_name, location, public_ip_addresses, idle_timeout_in_minutes, tags, zones=None):
    # Create Public IP Address if not provided
    if not public_ip_addresses:
        public_ip = network.PublicIPAddress(f"{nat_gateway_name}-pip",
                                            resource_group_name=resource_group_name,
                                            location=location,
                                            public_ip_allocation_method="Static",
                                            sku=network.PublicIPAddressSkuArgs(
            name="Standard"
        ),
            tags=tags)
        public_ip_addresses = [public_ip.id]

    # Create NAT Gateway
    nat_gateway = network.NatGateway(nat_gateway_name,
                                     resource_group_name=resource_group_name,
                                     location=location,
                                     public_ip_addresses=[
                                         network.SubResourceArgs(id=public_ip_id) for public_ip_id in public_ip_addresses
                                     ],
                                     idle_timeout_in_minutes=idle_timeout_in_minutes,
                                     sku=network.NatGatewaySkuArgs(
                                         name=network.NatGatewaySkuName.STANDARD
                                     ),
                                     zones=zones,
                                     tags=tags)

    return nat_gateway
