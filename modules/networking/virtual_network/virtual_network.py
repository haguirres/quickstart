import pulumi
import pulumi_azure_native as azure


def create_vnet(vnet_values: dict[str, any], resource_group_name: str, location: str, tags: dict[str, str]):
    virtual_network = azure.network.VirtualNetwork("virtualNetworl",
                                                   virtual_network_name=vnet_values["vnet_name"],
                                                   resource_group_name=resource_group_name,
                                                   location=location,
                                                   address_space=azure.network.AddressSpaceArgs(
                                                       address_prefixes=vnet_values["address_space"]),         
                                                    subnets=[{
                                                       "name": subnet["name"],
                                                       "addressPrefix": subnet["addressPrefix"]
                                                   }for subnet in vnet_values["subnets"]],                                          
                                                   tags=tags)

    return virtual_network
