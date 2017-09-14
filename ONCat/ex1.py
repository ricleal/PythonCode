import getpass
import os
import sys

import dotenv
import oauthlib
import requests_oauthlib
import requests

from pprint import pprint

dotenv.load_dotenv(dotenv.find_dotenv())

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

print("Username:")
username = sys.stdin.readline().strip()
password = getpass.getpass()


class TokenStore(object):
    '''
    One Token per user!
    '''

    oncat_token_url = 'https://oncat.ornl.gov/oauth/token'
    def __init__(self, username, password):
        '''
        Init is sort of a login on real website
        '''
        self._fetch_token(username, password)
        self._create_auto_refresh_client()

    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, val):
        self._token = val
    
    @token.deleter
    def token(self):  
        del self._token
    
    def _create_auth_client(self):
        initial_oauth_client = requests_oauthlib.OAuth2Session(
            client=oauthlib.oauth2.LegacyApplicationClient(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
            )
        )
        return initial_oauth_client
    
    def _fetch_token(self, username, password):
        '''
        Get a new token
        In a real system this is done at the Login
        '''
        initial_oauth_client = self._create_auth_client()
        self._token = initial_oauth_client.fetch_token(
            self.oncat_token_url,
            username=username,
            password=password,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )

    def _create_auto_refresh_client(self):
        self.client = requests_oauthlib.OAuth2Session(
            CLIENT_ID,
            token=self._token,
            auto_refresh_url=self.oncat_token_url,
            auto_refresh_kwargs={
                'client_id': CLIENT_ID,
            },
            token_updater=self.token,
        )

t = TokenStore(
    username,
    password,
)

try:
    result = t.client.get(
        'https://oncat.ornl.gov/api/experiments',
        params={
            'facility': 'SNS',
            'instrument': 'EQSANS',
            'projection': ['name'],
        },
    )
    result.raise_for_status()
    pprint(result.json())

except requests.HTTPError as error:
    if(error.response.status_code == 401 and
            'Bearer Token Not Found' in error.response.text):
        # Ignore this error
        pass

