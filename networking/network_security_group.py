import pulumi
import pulumi_azure_native as azure


def create_network_security_group(resource_group_name, nsg_name, location, tags, security_rules):
    print(security_rules)
    # Create a network security group
    nsg = azure.network.NetworkSecurityGroup(nsg_name,
                                             location=location,
                                             network_security_group_name=nsg_name,
                                             resource_group_name=resource_group_name,
                                             security_rules=[
                                                 azure.network.SecurityRuleArgs(
                                                     name=rule["name"],
                                                     priority=rule["priority"],
                                                     direction=rule["direction"],
                                                     access=rule["access"],
                                                     protocol=rule["protocol"],
                                                     source_port_range=rule["source_port_range"],
                                                     destination_port_range=rule["destination_port_range"],
                                                     source_address_prefix=rule["source_address_prefix"],
                                                     destination_address_prefix=rule["destination_address_prefix"]
                                                 ) for rule in security_rules
                                             ],
                                             tags=tags
                                             )
    return nsg
