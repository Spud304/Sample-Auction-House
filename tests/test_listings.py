import unittest
import pytest
import requests
import random
import names
import os
import tempfile
from src import main

from json import dumps, loads
from uuid import uuid4

@pytest.fixture
def client():
    db_fd, main.app.config['DATABASE'] = tempfile.mkstemp()
    main.app.config['TESTING'] = True

    with main.app.test_client() as client:
        with main.app.app_context():
            main.db.init_app(main.app)
        yield client

    os.close(db_fd)
    os.unlink(main.app.config['DATABASE'])


def _generate_listing() -> dict:
    return {
        'name': names.get_first_name(),
        'item_id': str(uuid4()),
        'buy_now': random.randint(1000, 2000),
        'seller': str(uuid4())
    }

def _generate_buy_request(item_id, money) -> dict:
    return {
        'item_id': item_id,
        'money': money,
        'user_id': str(uuid4())
    }

def test_health(client):
    rv = client.get('/_ah/health')
    assert(rv.status_code == 200)
    # response = client.get('/_ah/health')
    # assert(response.status_code, 200)

def test_create(client):
    body = _generate_listing()
    # response = client.post('/listings/create', json=dumps(body))
    rv = client.post('/listings/create', json=dumps(body))
    assert(rv.status_code == 201)


def test_get(client):
    body = _generate_listing()
    response = client.post('/listings/create', json=dumps(body))
    assert(response.status_code == 201)

    response = client.get('/listings/' + body['seller'])
    assert(response.status_code == 201)

    rJSON = response.json[0]
    assert(rJSON['name'] == body['name'])
    assert(rJSON['buy_now'] == body['buy_now'])
    assert(rJSON['seller'] == body['seller'])



def test_listing_does_not_exist(client):
    body = _generate_buy_request(str(uuid4()), money=random.randint(1, 100))
    response = client.post('/listings/buy/random_id', json=dumps(body))
    assert(response.status_code == 404)


def test_buy_without_enough_money(client):
    body = _generate_listing()
    response = client.post('/listings/create', json=dumps(body))
    assert(response.status_code == 201)

    # create a new highest bidder
    body2 = _generate_buy_request(body['seller'], money=body['buy_now'] - 10)
    response = client.post(f'/listings/buy/{body["item_id"]}', json=dumps(body2))
    assert(response.status_code == 200)
    assert(response.text == 'Listing updated')

    # try to bid without enough money
    body3 = _generate_buy_request(body['seller'], money=body['buy_now'] - 20)
    response = client.post(f'/listings/buy/{body["item_id"]}', json=dumps(body3))
    assert(response.status_code == 400)
    assert(response.text == 'Not enough money')


def test_update_bid_at_same_price(client):
    body = _generate_listing()
    response = client.post('/listings/create', json=dumps(body))
    assert(response.status_code == 201)

    # create a new highest bidder
    body2 = _generate_buy_request(body['seller'], money=body['buy_now'] - 10)
    response = client.post(f'/listings/buy/{body["item_id"]}', json=dumps(body2))
    assert(response.status_code == 200)
    assert(response.text == 'Listing updated')

    # try to bid without enough money
    body3 = _generate_buy_request(body['seller'], money=body['buy_now'] - 10)
    response = client.post(f'/listings/buy/{body["item_id"]}', json=dumps(body3))
    assert(response.status_code == 400)
    assert(response.text == 'Not enough money')

def test_buy_now(client):
    body = _generate_listing()
    response = client.post('/listings/create', json=dumps(body))
    assert(response.status_code == 201)

    # create a new highest bidder
    body2 = _generate_buy_request(body['seller'], money=body['buy_now'])
    response = client.post(f'/listings/buy/{body["item_id"]}', json=dumps(body2))
    assert(response.status_code == 200)
    assert(response.text == 'Listing bought')
    