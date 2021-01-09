#!/usr/bin/env python3
import http.client
import jwt
import json
from datetime import datetime, timedelta

from typing import NamedTuple, Dict, Union, cast

API_KEY_KEY = 'api_key'
API_SECRET_KEY = 'api_secret'

Creds = NamedTuple('Creds', [('key', str), ('secret', str)])

def read_credentails() -> Creds:
	raw_creds: Dict[str, str] = {}
	with open('zoom_creds', 'r') as cred_file:
		for line in cred_file.readlines():
			(key, value) = line.strip().split('=')
			raw_creds[key] = value

	key = raw_creds[API_KEY_KEY]
	secret = raw_creds[API_SECRET_KEY]

	return Creds(key, secret)

def generate_jwt(key: str, secret: str) -> str:
	expirey = datetime.utcnow() + timedelta(minutes=15)
	unix_expiry = expirey.strftime('%s')

	payload: Dict[str, str] = {'iss': key, 'exp': unix_expiry}

	encoded_jwt = jwt.encode(payload, secret, algorithm='HS256')

	return encoded_jwt


def new_meeting_request(valid_jwt: str) -> str:
	conn = http.client.HTTPSConnection('api.zoom.us')

	headers = {
		'authorization': f'Bearer {valid_jwt}',
		'content-type': 'application/json'
	}

	# by resquesting {} we just use all the defaults. 
	# type would shift from 90 days to 365
	# topic would rename it

	conn.request('POST', '/v2/users/me/meetings', body='{}', headers=headers)

	res = conn.getresponse()
	data_json = res.read().decode('utf-8')

	data: Dict[str, Union[str, int]] = json.loads(data_json)

	return cast(str, data['join_url'])


if __name__ == '__main__':
	key, secret = read_credentails()
	new_jwt = generate_jwt(key, secret)
	join_url = new_meeting_request(new_jwt)

	print(join_url)