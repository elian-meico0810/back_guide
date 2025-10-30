import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

load_dotenv()

def load_secrets() -> dict:    
    environment = os.getenv("ENVIRONMENT", "Production")

    if environment == "Develop":
        secrets = {
            "SECRET_KEY_2": os.getenv("SECRET_KEY_2"),
            "TENANT_ID": os.getenv("TENANT_ID"),
            "CLIENT_ID": os.getenv("CLIENT_ID"),
            "DBHOST": os.getenv("DBHOST"),
            "DBUSER": os.getenv("DBUSER"),
            "DBPASSWORD": os.getenv("DBPASSWORD"),
        }

        if os.environ.get('RUN_MAIN') == 'true':
            # ---------- 1. Autenticación con Azure ----------
            tenant_id = os.getenv("TENANT_ID")
            client_id = os.getenv("CLIENT_ID")
            client_secret = os.getenv("SECRET_KEY_2")
            vault_url = os.getenv("AZURE_KEYVAULT_URL")
            
            credential = ClientSecretCredential(tenant_id, client_id, client_secret)
            client = SecretClient(vault_url=vault_url, credential=credential)

            for secret_property in client.list_properties_of_secrets():
                secret_name = secret_property.name
                secret_value = client.get_secret(secret_name).value
                secrets[secret_name] = secret_value

        return secrets
    
    else:
        KEY_VAULT_NAME = "kv-secretosapp-pruebas"
        KV_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net/"

        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KV_URL, credential=credential)

        secret_keys = [
            "SECRET_KEY", "SECRET_KEY_2", 
            "TENANT_ID", "CLIENT_ID", "JWKS_URI", "ISSUER",
            "SECRET", "GOANYWHERE_USER", "GOANYWHERE_PASSWORD",
            "DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"
        ]

        secrets = {}
        for key in secret_keys:
            try:
                secrets[key] = client.get_secret(key).value
            except Exception as e:
                print(f"No se pudo obtener {key} desde Azure Key Vault. Error: {e}")

        return secrets
