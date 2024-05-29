import pulumi
from pulumi_azure_native import resources


def create_resource_group(resource_group_name, location, tags):
    resource_group = resources.ResourceGroup("resourceGroupResource",
                                             resource_group_name=resource_group_name,
                                             location=location,
                                             tags = tags)

    return resource_group
