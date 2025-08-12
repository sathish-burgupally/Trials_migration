import requests

from utilities import settings

port = 443



auth = (settings.username_db, settings.password)

url = f"https://{settings.host}/"  # OpenSearch root URL

print(url,auth)

response = requests.get(url, auth=auth, verify=True)
if response.status_code ==200:
    print("✅ OpenSearch connection established successfully")
    print(response.json())
else :
    print("❌ Failed to connect to OpenSearch")
    print("Status code :",response.status_code) 
    print("Error", response.text)



