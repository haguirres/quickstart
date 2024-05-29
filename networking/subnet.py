import pulumi
import pulumi_azure_native as azure


def create_subnet(vnet_name, resource_group_name, subnet_name, address_prefix, nsg, service_endpoints=[]):
    subnet = azure.network.Subnet(subnet_name,
                                  subnet_name=subnet_name,
                                  address_prefix=address_prefix,
                                  resource_group_name=resource_group_name,
                                  virtual_network_name=vnet_name,
                                  network_security_group=azure.network.NetworkSecurityGroupArgs(
                                      id=nsg.id
                                  ),
                                  service_endpoints=[
                                      azure.network.ServiceEndpointPropertiesFormatArgs(
                                          service=service
                                      ) for service in service_endpoints
                                  ]
                                  )
    return subnet
