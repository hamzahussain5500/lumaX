import requests
response = requests.get("http://192.168.102.101/api/status.json")
print(response.json())
