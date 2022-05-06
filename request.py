import requests
import smtplib 
import json
import re
from woocommerce import API
# https://example.com/wp-json/jwt-auth/v1/token
# print ("abcd")
# # http://localhost:81/projects/freelance/wordpress/wp-json
authurl = 'https://shop.roycetechnologies.co.ke/wp-json/jwt-auth/v1/token'
# authurl = 'https://shop.roycetechnologies.co.ke/wp-json/cocart/v2/login'
mainurl = 'https://shop.roycetechnologies.co.ke/wp-json/'
# url = 'http://localhost:81/projects/freelance/wordpress/wp-json/api/v1/token'
# myobj = {'somekey': 'somevalue'}

token= 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc2hvcC5yb3ljZXRlY2hub2xvZ2llcy5jby5rZSIsImlhdCI6MTY1MTQyNDEwNywibmJmIjoxNjUxNDI0MTA3LCJleHAiOjE2NTIwMjg5MDcsImRhdGEiOnsidXNlciI6eyJpZCI6MiwiZGV2aWNlIjoiIiwicGFzcyI6ImU5NjRlODY3ZTlkMjBiOWQwNjQxOGZkMDJhNzgyNTk3In19fQ.nus-YXBKxuNYJKSRmHoX8bq9gMYd7WN0Ec13lzbPZyM'
            # first_name= json_response['data']['firstName']
            

# endpoint =mainurl+ "cocart/v2/cart/items"
endpoint =mainurl+ "wp/v2/users/?search=josphat.kips@gmail.com"
# data = {"email": "josphat.kipse@gmail.com"}
# headers = {"Authorization": "Bearer "+token}

# response=requests.get(endpoint).json()
# print(response)
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
if(re.fullmatch(regex, 'josphat@gmail.com')):
        print("Valid Email")
 
else:
    print("Invalid Email")



# for key, value in response.items():
#    print(value['item_key'])
#    print(value['title'])
#    print(value['quantity']['value'])
#    print(value['totals']['subtotal'])
#    print(value['totals']['tax'])
#    print(value['totals']['total'])
#    print(value['featured_image'])
#    print(key, '->', value)

wcapi = API(
    url="https://shop.roycetechnologies.co.ke/",
    consumer_key="ck_15a2eb687f868ff4f5f0f47ce1b9a0d3b5b79450",
    consumer_secret="cs_80506487eb731aaf97b23cb2ba951a01b270c0b5",
    version="wc/v3"
)
res=wcapi.get("products?search=laptop", params={"per_page": 20}).json()
# for key, value in res.items():
#     print(value['id'])
myelements=[]
for re in res:
    # print(re)
   

    json_formatted_str = json.dumps(re, indent=2)

    # print(json_formatted_str)
    # build an object
    imgs=re['images'][0]
    newobj={
            "title": re['name'],
            "subtitle": re['name'],
            "image_url": imgs['src'],
            "buttons": [ 
                {
                "title": "Buy now",
                "url": re['permalink'],
                "type": "web_url"
                }
            ]
        }
    myelements.append(newobj)
message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": myelements
                
                }
        }
# print(message)



