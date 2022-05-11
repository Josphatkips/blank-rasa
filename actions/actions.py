# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
from typing import Any, Text, Dict, List
from woocommerce import API
from rasa_sdk.types import DomainDict
import re
import uuid
from rasa_sdk import Action, Tracker,FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset,FollowupAction
import requests
authurl = 'https://shop.roycetechnologies.co.ke/wp-json/jwt-auth/v1/token'
# authurl = 'https://shop.roycetechnologies.co.ke/wp-json/cocart/v2/login'
mainurl = 'https://shop.roycetechnologies.co.ke/wp-json/'


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_search_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

       
        data = {
            "username": tracker.get_slot('first_name'),
            "password": tracker.get_slot('last_name'),
           
        }


        dispatcher.utter_message(text = "Hello "+tracker.get_slot('last_name')+", Below is our checkout Link")
        dispatcher.utter_message(text = "https://shop.roycetechnologies.co.ke/checkout/")
        return []





       
        
        response = requests.post(authurl, json=data)
       
        json_response=response.json()
       

        # print (json_response['success'])
        
        if json_response['success']==False :

        
            # wrong password
            dispatcher.utter_message(text=json_response['message'])
            
            return [AllSlotsReset(),FollowupAction(name = "name_form")]
        else:
            # right password query cart
            # 
            token= json_response['data']['token']
            # token= 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc2hvcC5yb3ljZXRlY2hub2xvZ2llcy5jby5rZSIsImlhdCI6MTY1MTQyNDEwNywibmJmIjoxNjUxNDI0MTA3LCJleHAiOjE2NTIwMjg5MDcsImRhdGEiOnsidXNlciI6eyJpZCI6MiwiZGV2aWNlIjoiIiwicGFzcyI6ImU5NjRlODY3ZTlkMjBiOWQwNjQxOGZkMDJhNzgyNTk3In19fQ.nus-YXBKxuNYJKSRmHoX8bq9gMYd7WN0Ec13lzbPZyM'
            first_name= json_response['data']['firstName']
            # first_name= 'Josphat'

            dispatcher.utter_message(text="Hello "+first_name+" wait a moment as I process your request.")

            endpoint =mainurl+ "cocart/v2/cart/items"
            data = {"ip": "1.1.2.3"}
            headers = {"Authorization": "Bearer "+token}

            response=requests.get(endpoint, json=data, headers=headers).json()
            if  response=='No items in the cart.':
                
                dispatcher.utter_message(text="your cart is empty use the following link to order")
                dispatcher.utter_message(text = "https://shop.roycetechnologies.co.ke/")
                return []
           

            dispatcher.utter_message(text="Order details")
            for key, value in response.items():
                # print(value['item_key'])
                # print(value['title'])
                # print(value['quantity']['value'])
                # print(value['totals']['subtotal'])
                # print(value['totals']['tax'])
                # print(value['totals']['total'])
                # print(value['featured_image'])
                dispatcher.utter_message(text=value['title'])
                dispatcher.utter_message(text="Subtotal: "+str(value['totals']['subtotal']))
                dispatcher.utter_message(text="Tax: "+str(value['totals']['tax']))
                dispatcher.utter_message(text="Total: "+str(value['totals']['total']))
                dispatcher.utter_message(image = value['featured_image'])
                dispatcher.utter_message(text = "Click below link to checkout")
                dispatcher.utter_message(text = "https://shop.roycetechnologies.co.ke/checkout/")
                

        
            




        return []
# https://wordpress.org/plugins/custom-wp-rest-api/
# docker-compose pull && docker-compose up -d

class BuyProduct(Action):

    def name(self) -> Text:
        return "action_buy_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(text="This is purchase from action")
        wcapi = API(
        url="https://shop.roycetechnologies.co.ke/",
        consumer_key="ck_15a2eb687f868ff4f5f0f47ce1b9a0d3b5b79450",
        consumer_secret="cs_80506487eb731aaf97b23cb2ba951a01b270c0b5",
        version="wc/v3"
        )
        product=tracker.get_slot('product')
        res=wcapi.get("products?search="+product, params={"per_page": 20}).json()
        # for key, value in res.items():
        #     print(value['id'])
       
        if not res:
            dispatcher.utter_message(text ='I did not find product by that name, Kindly rephrase')
        myelements=[]
        for re in res:
            # print(re['permalink'])
            imgs=re['images'][0]
            newobj={
                    "title": re['name'],
                    "subtitle": re['description'],
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
            
            # dispatcher.utter_message(text ="Purchase link " + re['permalink'])
            # dispatcher.utter_message(text =re['description'])

            # for image in re['images']:
            #     dispatcher.utter_message(image = image['src'])
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": myelements
                
                }
        }
        dispatcher.utter_message(attachment=message)
        return []

            # dispatcher.utter_message(text ="Purchase link " + re['permalink'])
class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""

        # If the name is super short, it might be wrong.
        name = slot_value
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, slot_value)):
                # print("Valid Email")
                # dispatcher.utter_message(text="Enter a valid email address")
                
                return {"first_name": slot_value}
        
        else:
            dispatcher.utter_message(text="Enter a valid email address")
            return {"first_name": None}
        # if len(name) == 0:
        #     dispatcher.utter_message(text="That must've been a typo.")
        #     return {"first_name": None}
        # return {"first_name": name}

class ActionCarousel(Action):
    def name(self) -> Text:
        return "action_buy_productc"
    
    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Carousel 1",
                        "subtitle": "$10",
                        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqhmyBRCngkU_OKSL6gBQxCSH-cufgmZwb2w&usqp=CAU",
                        "buttons": [ 
                            {
                            "title": "Happy",
                            "payload": "Happy",
                            "type": "postback"
                            },
                            {
                            "title": "sad",
                            "payload": "sad",
                            "type": "postback"
                            }
                        ]
                    },
                    {
                        "title": "Carousel 2",
                        "subtitle": "$12",
                        "image_url": "https://image.freepik.com/free-vector/city-illustration_23-2147514701.jpg",
                        "buttons": [ 
                            {
                            "title": "Click here",
                            "url": "https://image.freepik.com/free-vector/city-illustration_23-2147514701.jpg",
                            "type": "web_url"
                            }
                        ]
                    }
                ]
                }
        }
        dispatcher.utter_message(attachment=message)
        return []



class ActionSaveConversation(Action):

    def name(self) -> Text:
        return "action_save_conversations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conversation=tracker.events
        # print(conversation)
        import os
        if not os.path.isfile('chats.csv'):
            with open('chats.csv','w') as file:
                file.write("intent,user_input,entity_name,entity_value,action,bot_reply\n")
        if not os.path.isfile('chats.txt'):
            with open('chats.txt','w') as file2:
                file2.write("intent,user_input,entity_name,entity_value,action,bot_reply\n")
        chat_data=''
        my_list = []
        uid=uuid.uuid4()
        for i in conversation:
            if i['event'] == 'user':
                payload = {
                'time_stamp': i['timestamp'], 
                'message': i['text'],
                'sender':i['event'],
                'uid':uid,
                'channel':i['input_channel']
                }
                r = requests.get('http://localhost:8000/api/savelogs', params=payload)
                chat_data+=i['parse_data']['intent']['name']+','+i['text']+','
                # print('user: {}'.format(i['text']))
                if len(i['parse_data']['entities']) > 0:
                    chat_data+=i['parse_data']['entities'][0]['entity']+','+i['parse_data']['entities'][0]['value']+','
                    # print('extra data:', i['parse_data']['entities'][0]['entity'], '=',
                    #       i['parse_data']['entities'][0]['value'])
                else:
                    chat_data+=",,"
            elif i['event'] == 'bot':
                # print('Bot: {}'.format(i['text']))
                # print('=================bot')
                # print(i)
                # print('=================bot')
                payload = {
                'time_stamp': i['timestamp'], 
                'message': i['text'],
                'sender':i['event'],
                'uid':uid,
                # 'channel':i['input_channel']
                }
                r = requests.get('http://localhost:8000/api/savelogs', params=payload)
                try:
                    chat_data+=i['metadata']['utter_action']+','+i['text']+'\n'
                except KeyError:
                    pass
        else:
            # print(chat_data)
            with open('chats.csv','a') as file:
                file.write(chat_data)
            with open('chats.txt','a') as file2:
                file2.write(chat_data)

        # dispatcher.utter_message(text="All Chats saved.")

        return []

