import boto3
import json
from Custom_encoder import CustomEncoder
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'product-inventory'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'
healthpath = '/health'
product = '/product'
products = '/products'

def lamda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == healthpath
        response = buildResponse(200)
    elif httpMethod == getMethod and path == Productpath:
        response = getproduct(event['querystringParameters']['productId'])
    elif httpMethod == getMethod and path == productspath:
        response = getProducts()
    elif httpMethod == postMethod and path == productpath:
        response = getProducts()
    elif httpMethod == postMethod and path == productpath:
        response = saveproducts(json.loads(event['body']))
    elif httpMethod == patchMethod and path == productpath:
        requestBody = json.loads(event['body'])
        response = modifyproduct(requestBody['productId'], requestBody['updatekey'], requestBody['updatevalue'])
    elif httpMethod == deleteMethod and path == productpath:
        requestBody = json.loads(event['body'])
        response = deleteproduct(requestBody['productid'])
    else:
        response = buildResponse(484, 'Not Found')
    return response

def getproduct(productId):
    try:
        response = table.get_item(
            key={
                'productId': productId
            }
        )
        if 'item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(484, {'Message': 'productId: %s not found' % productId})
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!!')
def getproducts():
    try:
        response = table.scan()
        result = response['Item']

        while 'LastEvaluatedkey' in response:
            response = table.scan(ExclusiveStartkey=response['LastEvaluatedkey'])
            result.extend(response['Item'])

        body = {
            'products': response
        }
        return buildResponse(200, body)
    except:
         logger.exception('Do your custom error handling here. I am just gonna log it out here!!')

def modifyproduct(productId, updatekey, updateValue):
    try:
        response = table.update_item(
            key={
                'productId':productId
            },
            updateExpression='set %s = :value' % updatekey,
            ExpressionAttributeValues={
                ':value': updateValue
            
        },
        ReturnValues='UPDATED_NEW'
        )
        body = {
            'operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttrebutes': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!!')

def deleteproduct(productId):
    try:
        response = table.delete_item(
            key={
                'productId': productId
            }
            ReturnValues='All_OLD'
        )
        body = {
            'operation':'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response

        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!!')

def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statuscode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
        return response