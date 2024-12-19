#!/usr/bin/env python3
import http.client
import jwt
import json
import requests
from datetime import datetime, timedelta

from typing import NamedTuple, Dict, Union, cast

ACCOUNT_ID_KEY = 'account_id'
CLIENT_ID_KEY = 'client_id'
CLIENT_SECRET_KEY = 'client_secret'

AUTH_TOKEN_URL = 'https://zoom.us/oauth/token'
API_BASE_URL = 'https://api.zoom.us/v2'

Creds = NamedTuple('Creds', [('account_id', str), ('client_id', str), ('client_secret', str)])

def read_credentails() -> Creds:
	raw_creds: Dict[str, str] = {}
	with open('zoom_creds', 'r') as cred_file:
		for line in cred_file.readlines():
			(key, value) = line.strip().split('=')
			raw_creds[key] = value

	account_id = raw_creds[ACCOUNT_ID_KEY]
	client_id = raw_creds[CLIENT_ID_KEY]
	client_secret = raw_creds[CLIENT_SECRET_KEY]

	return Creds(account_id, client_id, client_secret)

def get_authorized_creds(app_creds: Creds) -> str:

	auth_params: Dict[str, Union[str, Dict[str, bool]]] = {
		"grant_type": "account_credentials",
		"account_id": app_creds.account_id,
		"client_secret": app_creds.client_secret
	}

	response = requests.post(AUTH_TOKEN_URL,
                                 auth=(app_creds.client_id, app_creds.client_secret),
                                 data=auth_params)

	if response.status_code!=200:
		print(response.text)
		raise Exception('Unable to get access token')

	response_data: Dict[str, str] = response.json()
	access_token = response_data['access_token']

	if not access_token:
		print(response.text)
		raise Exception('No token provided')

	return access_token

def create_new_meeting_url(access_token: str) -> str:

	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json"
	}
	meeting_args = {
		'topic': 'MacRae\'s Zoom Meeting',
		# 'schedule_for': 'macrae@truss.works',
		# 'start_time': f'{start_date}T10:{start_time}',
		# "type": 2
		'settings': {
			'use_pmi': False,
		}
	}

	resp = requests.post(f"{API_BASE_URL}/users/me/meetings",
										headers=headers,
										json=meeting_args)

	if resp.status_code!=201:
		print(resp.text)
		raise Exception('Unable to create meeting')

	payload: Dict[str,str] = resp.json()

	join_url = payload['join_url']

	return join_url

if __name__ == '__main__':
	app_creds = read_credentails()
	req_creds = get_authorized_creds(app_creds)
	new_url = create_new_meeting_url(req_creds)

	print(new_url)
