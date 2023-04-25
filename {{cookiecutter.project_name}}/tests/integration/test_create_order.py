import json
from http import HTTPStatus
from typing import Any, Dict

import boto3
from aws_lambda_powertools.utilities.feature_flags.exceptions import SchemaValidationError
from botocore.stub import Stubber

from service.dal.dynamo_dal_handler import DynamoDalHandler
from service.handlers.create_order import create_order
from service.handlers.schemas.input import Input
from tests.utils import generate_api_gw_event, generate_context





def test_handler_200_ok(table_name: str):

    customer_name = 'RanTheBuilder'
    order_item_count = 5
    body = Input(customer_name=customer_name, order_item_count=order_item_count)
    response = create_order(generate_api_gw_event(body.dict()), generate_context())
    # assert response
    assert response['statusCode'] == HTTPStatus.OK
    body_dict = json.loads(response['body'])
    assert body_dict['order_id']
    assert body_dict['customer_name'] == customer_name
    assert body_dict['order_item_count'] == 5
    # assert side effect - DynamoDB table
    dynamodb_table = boto3.resource('dynamodb').Table(table_name)
    response = dynamodb_table.get_item(Key={'order_id': body_dict['order_id']})
    assert 'Item' in response  # order was found
    assert response['Item']['customer_name'] == customer_name
    assert response['Item']['order_item_count'] == order_item_count


def test_internal_server_error():
    db_handler: DynamoDalHandler = DynamoDalHandler('table')
    table = db_handler._get_db_handler()
    stubber = Stubber(table.meta.client)
    stubber.add_client_error(method='put_item', service_error_code='ValidationException')
    stubber.activate()
    body = Input(customer_name='RanTheBuilder', order_item_count=5)
    response = create_order(generate_api_gw_event(body.dict()), generate_context())
    assert response['statusCode'] == HTTPStatus.INTERNAL_SERVER_ERROR


def test_handler_bad_request(mocker):
    response = create_order(generate_api_gw_event({'order_item_count': 5}), generate_context())
    assert response['statusCode'] == HTTPStatus.BAD_REQUEST
    body_dict = json.loads(response['body'])
    assert body_dict == {}


def test_handler_failed_appconfig_fetch(mocker):
    response = create_order(generate_api_gw_event({'order_item_count': 5}), generate_context())
    assert response['statusCode'] == HTTPStatus.INTERNAL_SERVER_ERROR
    body_dict = json.loads(response['body'])
    assert body_dict == {}
