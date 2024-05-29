import pulumi
import pulumi_azure_native as azure


def create_virtual_network(resource_group_name, location, tags,
                           vnet_name, address_space, dns_servers,
                           flow_timeout_in_minutes,  encryption, enable_vm_protection, enable_ddos_protection, ddos_protection_plan_id=None):

    virtual_network = azure.network.VirtualNetwork("virtualNetwork",
                                                   virtual_network_name=vnet_name,
                                                   resource_group_name=resource_group_name,
                                                   location=location,
                                                   dhcp_options={
                                                       "dnsServers": dns_servers
                                                   },
                                                   address_space={
                                                       "address_prefixes": address_space
                                                   },
                                                   enable_ddos_protection=enable_ddos_protection,
                                                   ddos_protection_plan=azure.network.VirtualNetworkDdosProtectionPlanArgs(
                                                       id=ddos_protection_plan_id
                                                   ) if enable_ddos_protection and ddos_protection_plan_id else None,
                                                   enable_vm_protection=enable_vm_protection,
                                                   encryption=encryption,
                                                   flow_timeout_in_minutes=flow_timeout_in_minutes,
                                                   tags=tags
                                                   )
    return virtual_network
