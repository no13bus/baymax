# -*- coding: utf-8 -*-
import requests
import json
import datetime
try:
    from urllib.parse import urlencode
except ImportError:
    # Python 2.x
    from urllib import urlencode
from requests_oauthlib import OAuth1, OAuth1Session
from .exceptions import (BadResponse, DeleteError, HTTPBadRequest,
                               HTTPUnauthorized, HTTPForbidden,
                               HTTPServerError, HTTPConflict, HTTPNotFound,
                               HTTPTooManyRequests)

class FitbitOauthClient(object):
    API_ENDPOINT = "https://api.fitbit.com"
    AUTHORIZE_ENDPOINT = "https://www.fitbit.com"
    API_VERSION = 1

    request_token_url = "%s/oauth/request_token" % API_ENDPOINT
    access_token_url = "%s/oauth/access_token" % API_ENDPOINT
    authorization_url = "%s/oauth/authorize" % AUTHORIZE_ENDPOINT

    def __init__(self, client_key, client_secret, resource_owner_key=None,
                 resource_owner_secret=None, user_id=None, callback_uri=None,
                 *args, **kwargs):
        """
        Create a FitbitOauthClient object. Specify the first 5 parameters if
        you have them to access user data. Specify just the first 2 parameters
        to access anonymous data and start the set up for user authorization.
        Set callback_uri to a URL and when the user has granted us access at
        the fitbit site, fitbit will redirect them to the URL you passed.  This
        is how we get back the magic verifier string from fitbit if we're a web
        app. If we don't pass it, then fitbit will just display the verifier
        string for the user to copy and we'll have to ask them to paste it for
        us and read it that way.
        """

        self.session = requests.Session()
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        if user_id:
            self.user_id = user_id
        params = {'client_secret': client_secret}
        if callback_uri:
            params['callback_uri'] = callback_uri
        if self.resource_owner_key and self.resource_owner_secret:
            params['resource_owner_key'] = self.resource_owner_key
            params['resource_owner_secret'] = self.resource_owner_secret
        self.oauth = OAuth1Session(client_key, **params)

    def _request(self, method, url, **kwargs):
        """
        A simple wrapper around requests.
        """
        return self.session.request(method, url, **kwargs)

    def make_request(self, url, data={}, method=None, **kwargs):
        """
        Builds and makes the OAuth Request, catches errors
        https://wiki.fitbit.com/display/API/API+Response+Format+And+Errors
        """
        if not method:
            method = 'POST' if data else 'GET'
        auth = OAuth1(
            self.client_key, self.client_secret, self.resource_owner_key,
            self.resource_owner_secret, signature_type='auth_header')
        response = self._request(method, url, data=data, auth=auth, **kwargs)

        if response.status_code == 401:
            raise HTTPUnauthorized(response)
        elif response.status_code == 403:
            raise HTTPForbidden(response)
        elif response.status_code == 404:
            raise HTTPNotFound(response)
        elif response.status_code == 409:
            raise HTTPConflict(response)
        elif response.status_code == 429:
            exc = HTTPTooManyRequests(response)
            exc.retry_after_secs = int(response.headers['Retry-After'])
            raise exc

        elif response.status_code >= 500:
            raise HTTPServerError(response)
        elif response.status_code >= 400:
            raise HTTPBadRequest(response)
        return response

    def fetch_request_token(self):
        """
        Step 1 of getting authorized to access a user's data at fitbit: this
        makes a signed request to fitbit to get a token to use in step 3.
        Returns that token.}
        """

        token = self.oauth.fetch_request_token(self.request_token_url)
        self.resource_owner_key = token.get('oauth_token')
        self.resource_owner_secret = token.get('oauth_token_secret')
        return token

    def authorize_token_url(self, **kwargs):
        """Step 2: Return the URL the user needs to go to in order to grant us
        authorization to look at their data.  Then redirect the user to that
        URL, open their browser to it, or tell them to copy the URL into their
        browser.  Allow the client to request the mobile display by passing
        the display='touch' argument.
        """

        return self.oauth.authorization_url(self.authorization_url, **kwargs)

    def fetch_access_token(self, verifier, token=None):
        """Step 3: Given the verifier from fitbit, and optionally a token from
        step 1 (not necessary if using the same FitbitOAuthClient object) calls
        fitbit again and returns an access token object. Extract the needed
        information from that and save it to use in future API calls.
        """
        if token:
            self.resource_owner_key = token.get('oauth_token')
            self.resource_owner_secret = token.get('oauth_token_secret')

        self.oauth = OAuth1Session(
            self.client_key,
            client_secret=self.client_secret,
            resource_owner_key=self.resource_owner_key,
            resource_owner_secret=self.resource_owner_secret,
            verifier=verifier)
        response = self.oauth.fetch_access_token(self.access_token_url)

        self.user_id = response.get('encoded_user_id')
        self.resource_owner_key = response.get('oauth_token')
        self.resource_owner_secret = response.get('oauth_token_secret')
        return response

# Client (Consumer) Key
# 0ad642de85bc4e30a5c1e0aca8ec8355
# Client (Consumer) Secret
# 018285a1459844c082e9e0711328bd66
# Temporary Credentials (Request Token) URL
# https://api.fitbit.com/oauth/request_token
# Token Credentials (Access Token) URL
# https://api.fitbit.com/oauth/access_token
# Authorize URL
# https://www.fitbit.com/oauth/authorize

if __name__ == '__main__':
    client = FitbitOauthClient(client_key='0ad642de85bc4e30a5c1e0aca8ec8355', client_secret='018285a1459844c082e9e0711328bd66',
                      callback_uri='http://baymax.ninja/callback')
    token = client.fetch_request_token()
    should_open_url = client.authorize_token_url()
    # http://baymax.ninja/callback?oauth_token=88146d78f39d8b869c33d7488cf0ea0d&oauth_verifier=f978e667ba172c9a0c71a4c5bab98e29
    new_token = client.fetch_access_token('f978e667ba172c9a0c71a4c5bab98e29')
    # 得到uid resource_owner_key 和 secret