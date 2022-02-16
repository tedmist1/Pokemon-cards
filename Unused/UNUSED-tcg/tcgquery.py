import requests

Application_Id = 10647
public_key = "d32b16ed-1f5a-4ce6-9339-8272f476417b"
private_key = "5ee20512-983d-45a1-96a6-d2d267acc269"

response = requests.post(
            "https://api.tcgplayer.com/token",
            
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"},
           
            data=(f"grant_type=client_credentials"
                  f"&client_id={public_key}&"
                  f"client_secret={private_key}")
        )

access = response.json()['access_token'];

headers = {"accept": "application/json", 
           "Content-Type": "application/json",
           'User-Agent': 'YOUR_USER_AGENT',
           "Authorization": "bearer " + access}


# url = "https://api.tcgplayer.com/catalog/categories"
# response = requests.get(url, headers=headers)
# print(response.json())


# Pokemon is 3

# Find the products using pokemon (3)
# url = "https://api.tcgplayer.com/catalog/categories/3/search"
# payload = {"sort":"Relevance",
#            "filters": [{
#               "values": ["Celebrations Elite Trainer Box"],
#               "name": "productName"
#           }]}
# search_response = requests.request("POST", url, json=payload, headers=headers)
# print(search_response.json())





endpoint = "https://api.tcgplayer.com/catalog/products/"
# productids = str(search_response.json()["results"])

# Celebrations ETB id: 242811
celebrations = "242811"
url = endpoint + celebrations # endpoint + productids
response = requests.get( url, headers=headers)
print(response.json())



# url = "https://example.com/pricing/buy/product/242811"

# response = requests.request("GET", url)

# print(response.text)





'''
url = "https://api.tcgplayer.com/pricing/buy/sku/skuIds"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

print(response.text)
'''