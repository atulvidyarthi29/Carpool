# lambda function for lex confirm.


import json
import boto3
import time
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    ttype = event["currentIntent"]["slots"]["type"]
    days = event["currentIntent"]["slots"]["days"]
    place = event["currentIntent"]["slots"]["place"]
    payment = event["currentIntent"]["slots"]["payment"]
    pickup = event["currentIntent"]["slots"]["pickup"]
    carid = event["currentIntent"]["slots"]["carid"]
    orderdate = str(datetime.today())
    
    dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
    table = dynamodb.Table('orders')
    cars = dynamodb.Table('cars')
    if not(carid):
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
        table = dynamodb.Table('orders')
        cars = dynamodb.Table('cars')
        table = dynamodb.Table('orders')
        caridboi = cars.scan(FilterExpression=Attr('cartype').eq(ttype.lower()))
        items = caridboi['Items']
        content = ""
        idlist = []
        carcompany = []
        priceperday = []
        DOM = []
        for i in items:
            idlist.append(i["carid"])
            carcompany.append(i["carcompany"])
            priceperday.append(i["priceperday"])
            DOM.append(i["DOM"])
        content = "We have the following models available for you : \n"
        for i in range(len(DOM)):
            content = content+str(idlist[i])+". "+carcompany[i]+" model "+str(DOM[i])+" for the price of "+str(priceperday[i])+" per day.\n" 
        content = content + "Please enter the number of the car that you prefer : \n"
        response = {
        "dialogAction": {
            "type": "ElicitSlot",
            "message": {
                "contentType": "PlainText",
                "content": content
                },
            "intentName":"RentACar",
            "slots": {
                "type": ttype.lower(),
                "days": days,
                "place": place,
                "payment": payment,
                "pickup": pickup,
                },
            "slotToElicit": "carid"
            }
        }
    else:
        thecar = cars.get_item(Key={'carid': int(carid)})
        table.put_item(
            Item={
                'id': int(time.time()),
                'days': days,
                'place': place,
                'payment_type': payment,
                'pickup_date': pickup,
                'username': 'iiits',
                'carid': thecar["Item"],
                'order_date': orderdate
                }
            )   
        response = {
            "dialogAction": {
                "type" : "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Thanks, your order has been placed."
                    }
                }
        }
    return response