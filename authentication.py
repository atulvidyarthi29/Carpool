import boto3
import hmac
import hashlib
import base64

USER_POOL_ID = 'us-east-1_wZZ7wrox7'
CLIENT_ID = '75ckbdj1hlkhbc42usmq1e0jn7'
CLIENT_SECRET = 'qkfshu8u2dhg1mo72iupm0likbkpsn7m6536hfnvrv5de3kdds3'

client = boto3.client('cognito-idp')


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


# login

def login(username, password):
    resp, msg = initiate_auth(username, password)
    if msg is not None:
        return {'message': msg,
                "error": True, "success": False, "data": None}
    if resp.get("AuthenticationResult"):
        return {'message': "success",
                "error": False,
                "success": True,
                "data": {
                    "id_token": resp["AuthenticationResult"]["IdToken"],
                    "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                    "access_token": resp["AuthenticationResult"]["AccessToken"],
                    "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                    "token_type": resp["AuthenticationResult"]["TokenType"],
                },
                }
    else:  # this code block is relevant only when MFA is enabled
        return {"error": True,
                "success": False,
                "data": None, "message": None}


def initiate_auth(username, password):
    secret_hash = get_secret_hash(username)
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': secret_hash,
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': username,
                'password': password,
            })
    except client.exceptions.NotAuthorizedException:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
    return resp, None


# registration

def registration(event):
    for field in ["username", "email", "password", "name"]:
        if not event.get(field):
            return {"error": False, "success": True, 'message': f"{field} is not present", "data": None}
    username = event['username']
    email = event["email"]
    password = event['password']
    name = event["name"]
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': "name",
                    'Value': name
                },
                {
                    'Name': "email",
                    'Value': email
                }
            ],
            ValidationData=[
                {
                    'Name': "email",
                    'Value': email
                },
                {
                    'Name': "custom:username",
                    'Value': username
                }
            ])
    except client.exceptions.UsernameExistsException as e:
        return {"error": True,
                "success": False,
                "message": "This username already exists",
                "data": None}
    except client.exceptions.InvalidPasswordException as e:

        return {"error": True,
                "success": False,
                "message": "Password should have Caps,\
                          Special chars, Numbers",
                "data": None}
    except client.exceptions.UserLambdaValidationException as e:
        return {"error": True,
                "success": False,
                "message": "Email already exists",
                "data": None}

    except Exception as e:
        return {"error": True,
                "success": False,
                "message": str(e),
                "data": None}

    return {"error": False,
            "success": True,
            "message": "Please confirm your signup,check Email for validation code",
            "data": None}
