import pulumi
import pulumi_azure_native as azure


def create_key_vault(key_vault_name, resource_group, location, properties, tags):
    key_vault = azure.keyvault.Vault(key_vault_name,
                                     resource_group_name=resource_group.name,
                                     location=location,
                                     properties=azure.keyvault.VaultPropertiesArgs(
                                         tenant_id=properties["tenantId"],
                                         soft_delete_retention_in_days=properties[
                                             "soft_delete_retention_in_days"],
                                         enabled_for_deployment=properties["enabled_for_deployment"],
                                         enabled_for_disk_encryption=properties["enabled_for_disk_encryption"],
                                         enabled_for_template_deployment=properties[
                                             "enabled_for_template_deployment"],
                                         sku=azure.keyvault.SkuArgs(
                                             family=properties["skuFamily"],
                                             name=properties["skuName"]
                                         )
                                     ),
                                     vault_name=key_vault_name,
                                     tags=tags
                                     )

    return key_vault
