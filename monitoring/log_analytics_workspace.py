import pulumi
from pulumi_azure_native import operationalinsights


def create_log_analytics_workspace(workspace_name, resource_group, location, sku, retention_in_days, tags):
    workspace = operationalinsights.Workspace(workspace_name,
                                              resource_group_name=resource_group.name,
                                              location=location,
                                              sku=sku,
                                              retention_in_days=retention_in_days,
                                              tags=tags)

    return workspace
