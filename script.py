import requests
from azure.identity import DefaultAzureCredential

# Azure details
subscription_id = "14ffaa1d-0aab-4e18-ae88-27ebc1732b10"
resource_group_name = "rg-manageit-argus-prod"
cluster_name = "db-psql-clstercosmos-manageit-argus-prod"

# Base URL for Azure Resource Manager
base_url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.DBforPostgreSQL/serverGroupsv2/{cluster_name}"

# SKU configurations
burstable_tier1 = {
    "sku": {
        "name": "Standard_B1ms",  # Burstable 1 vCore, 2 GiB RAM
        "tier": "Burstable"
    }
}
burstable_tier2 = {
    "sku": {
        "name": "Standard_B2ms",  # Burstable 2 vCores, 4 GiB RAM
        "tier": "Burstable"
    }
}

def scale_cluster(sku):
    """Scale the Azure Cosmos DB PostgreSQL cluster to the desired SKU."""
    # Obtain access token using DefaultAzureCredential
    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default").token

    # Headers for the REST API request
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # REST API URL for updating the cluster
    update_url = f"{base_url}?api-version=2023-03-02-preview"

    # Make the HTTP PATCH request to scale the cluster
    response = requests.patch(update_url, headers=headers, json=sku)

    if response.status_code in (200, 202):
        print(f"Cluster scaling initiated successfully to: {sku['sku']['name']}")
    else:
        print(f"Failed to scale the cluster: {response.status_code} - {response.text}")
        response.raise_for_status()

def main():
    import datetime
    current_hour = datetime.datetime.utcnow().hour

    # Peak hours (9 AM to 5 PM UTC)
    if 8 <= current_hour < 17:
        print("Peak hours detected. Scaling to 2 vCores, 4 GiB RAM.")
        scale_cluster(burstable_tier2)
    else:
        print("Off-peak hours detected. Scaling to 1 vCore, 2 GiB RAM.")
        scale_cluster(burstable_tier1)

if __name__ == "__main__":
    main()
