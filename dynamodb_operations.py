import boto3
from botocore.exceptions import ClientError as e
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")


def rent_car(item):
    try:
        table = dynamodb.Table('orders')
        response = table.put_item(
            Item=item
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


def get_bookings(username):
    table = dynamodb.Table('orders')
    response = table.scan(
        FilterExpression=Attr('username').eq(username)
    )
    items = response['Items']
    return items


def modify_bookings(id):
    try:
        table = dynamodb.Table('orders')
        response = table.update_item(
            Key={
                'id': id,
            },
            UpdateExpression="set info.rating=:r, info.plot=:p, info.actors=:a",
        )
        print(response)
        return response
    except e:
        return {
            'success': False,
            'error': True,
            'message': "Your bookings could not be fetched. Some problem occurred."}


def delete_booking(id):
    table = dynamodb.Table('orders')
    response = table.delete_item(Key={
        'id': id,
    })
    return response


def get_all_cars():
    try:
        table = dynamodb.Table('cars')
        response = table.scan()
        return response
    except e:
        return {
            'success': False,
            'error': True,
            'message': "Some problem occurred."}


def get_car(id):
    try:
        table = dynamodb.Table('cars')
        response = table.get_item(Key={
            'carid': id,
        })
        return response
    except e:
        return {
            'success': False,
            'error': True,
            'message': "Some problem occurred."}
