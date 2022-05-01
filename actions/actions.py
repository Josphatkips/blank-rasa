# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
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

       
        
        response = requests.post(authurl, json=data)
       
        json_response=response.json()
       

        print (json_response['success'])
        
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