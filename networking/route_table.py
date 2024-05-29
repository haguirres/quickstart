import pulumi
from pulumi_azure_native import network


def create_route_table(resource_group, route_table_name, location, tags, routes=[]):
    # Create the Route Table
    route_table = network.RouteTable(route_table_name,
                                     route_table_name=route_table_name,
                                     resource_group_name=resource_group.name,
                                     location=location,
                                     routes=[network.RouteArgs(
                                         name=route["name"],
                                         address_prefix=route["address_prefix"],
                                         next_hop_type=route["next_hop_type"],
                                         next_hop_ip_address=route["next_hop_ip_address"]
                                     ) for route in routes],
                                     tags=tags)
