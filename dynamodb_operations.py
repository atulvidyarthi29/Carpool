import boto3
from botocore.exceptions import ClientError as e

dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")


def rent_car(item_details):
    try:
        table = dynamodb.Table('orders')
        response = table.put_item(
            Item={
                'id': 10,
                'pickup_address': item_details['pickup_address'],
                'pick_up_date': item_details['pickup_date'],
                'order_date': item_details['order_date'],
                'car_type': item_details['car_type'],
                'car_company': item_details['car_company'],
                'payment_type': item_details['payment_type'],
                'username': item_details['username'],
            }
        )
        return {
            'success': True,
            'error': False,
            'message': "Successfully booked the item."
        }
    except e:
        return {
            'success': False,
            'error': True,
            'message': f"Unknown error {e.__dict__}"
        }


def get_all_cars():
    try:
        table = dynamodb.Table('cars')
        response = table.scan()
        return response
    except e:
        return {
            'success': False,
            'error': True,
            'message': ""}



