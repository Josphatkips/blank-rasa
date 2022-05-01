import requests
import smtplib 
# https://example.com/wp-json/jwt-auth/v1/token
# print ("abcd")
# # http://localhost:81/projects/freelance/wordpress/wp-json
authurl = 'https://shop.roycetechnologies.co.ke/wp-json/jwt-auth/v1/token'
# authurl = 'https://shop.roycetechnologies.co.ke/wp-json/cocart/v2/login'
mainurl = 'https://shop.roycetechnologies.co.ke/wp-json/'
# url = 'http://localhost:81/projects/freelance/wordpress/wp-json/api/v1/token'
# myobj = {'somekey': 'somevalue'}

# x = requests.post(url, data = myobj)

# 
# josphat.kips@gmail.com
# Kenya2030!

# print(x.text)
# data = {
#     "username": 'josphat.kips@gmail.com',
#     "password": "Kenya2030!",
#     # "username": 'admin@shop.roycetechnologies.co.ke',
#     # "password": "Kenya#2030!?!",
#     # "passion": "coding",
# }
 
# response = requests.post(authurl, json=data)
 
# print("Status Code", response.status_code)
# print("JSON Response ", response.json())






token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc2hvcC5yb3ljZXRlY2hub2xvZ2llcy5jby5rZSIsImlhdCI6MTY1MTMxNzIyNSwibmJmIjoxNjUxMzE3MjI1LCJleHAiOjE2NTE5MjIwMjUsImRhdGEiOnsidXNlciI6eyJpZCI6MiwiZGV2aWNlIjoiIiwicGFzcyI6ImU5NjRlODY3ZTlkMjBiOWQwNjQxOGZkMDJhNzgyNTk3In19fQ.Qs3TqCDR8rSQlgVslwfJwjNg_RpsnbNiaBtVWF2QtQs"


# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc2hvcC5yb3ljZXRlY2hub2xvZ2llcy5jby5rZSIsImlhdCI6MTY1MTMyMTk0OCwibmJmIjoxNjUxMzIxOTQ4LCJleHAiOjE2NTE5MjY3NDgsImRhdGEiOnsidXNlciI6eyJpZCI6MSwiZGV2aWNlIjoiIiwicGFzcyI6IjFlODdmZDlkOGE2MGI0NjM4NWViZDk3MjRiNGVkNWE2In19fQ.G5_Ks-j2aCbZmqaVaZ_SS04qJ7wQHVLUK4MgGRO7TbI
endpoint =mainurl+ "cocart/v2/cart/items"
data = {"ip": "1.1.2.3"}
headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc2hvcC5yb3ljZXRlY2hub2xvZ2llcy5jby5rZSIsImlhdCI6MTY1MTMyMzA1NCwibmJmIjoxNjUxMzIzMDU0LCJleHAiOjE2NTE5Mjc4NTQsImRhdGEiOnsidXNlciI6eyJpZCI6MiwiZGV2aWNlIjoiIiwicGFzcyI6ImU5NjRlODY3ZTlkMjBiOWQwNjQxOGZkMDJhNzgyNTk3In19fQ.wFMVs_UZVGB7UtfEqo3qngifevvac0BNWG8BytAvJGQ"}

print(requests.get(endpoint, data=data, headers=headers).json())





