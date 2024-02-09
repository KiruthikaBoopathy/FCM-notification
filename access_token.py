# from msal import ConfidentialClientApplication
import requests
import time
import msal
from msal import ConfidentialClientApplication
import os
import requests
import webbrowser

# outlook_id = 'kiruthika.b@vrdella.com'
app_id= "7f17aca3-6b3e-4740-a733-09cc1a77518c"
client_secret = "qms8Q~zmxHt6eUJ5qjMseMGEcKubik7AtCpK6cKd"
tenant_id = "808cc74b-8f92-457a-a47a-2cbf60972a27"
SCOPES = ["https://graph.microsoft.com/.default"]
authority = f'https://login.microsoftonline.com/{tenant_id}'


email = 'kowsalya@vrdella.com'
cache_file_path = f'token_cache_{email.replace("@", "_").replace(".", "_")}.bin'

token_cache = msal.SerializableTokenCache()
if os.path.exists(cache_file_path):
    token_cache.deserialize(open(cache_file_path, "r").read())

client = ConfidentialClientApplication(
    client_id=app_id,
    client_credential=client_secret,
    token_cache=token_cache
)

accounts = client.get_accounts()
if accounts:
    result = client.acquire_token_silent(SCOPES, account=accounts[0])
    print(result)
    access_token = result.get("access_token")

else:
    authorization_url = client.get_authorization_request_url(SCOPES)
    webbrowser.open(authorization_url)
    authorization_code = input("Enter the authorization code: ")
    result = client.acquire_token_by_authorization_code(authorization_code, SCOPES)
    result.get('scope', '')
    access_token = result.get("access_token")

open(cache_file_path, "w").write(token_cache.serialize())
