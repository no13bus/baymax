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

# API Key	055ce4ef5b191b81750f46008d7f0dfd421f37d97bf4554eff4d1369c5
# API Secret	0737e7fe7214d40f891f201250718445944c1447e677cb5b193799e3f


class WithingsOauthClient(object):
    API_ENDPOINT = "https://api.fitbit.com"
    AUTHORIZE_ENDPOINT = "https://www.fitbit.com"
    API_VERSION = 1

    request_token_url = "https://oauth.withings.com/account/request_token"
    access_token_url = "https://oauth.withings.com/account/access_token"
    authorization_url = "https://oauth.withings.com/account/authorize"

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

if __name__ == '__main__':
    client = WithingsOauthClient(client_key='055ce4ef5b191b81750f46008d7f0dfd421f37d97bf4554eff4d1369c5', client_secret='0737e7fe7214d40f891f201250718445944c1447e677cb5b193799e3f',
                      callback_uri='http://baymax.ninja/callback')
    token = client.fetch_request_token()
    should_open_url = client.authorize_token_url()
    # http://baymax.ninja/callback?userid=6828098&oauth_token=8f9c49e207b3389d5c034bd68ede0fb5dcfcf61f218bf6e733135d19f4e359&oauth_verifier=I85jvp5yJHKhzliH
    new_token = client.fetch_access_token('I85jvp5yJHKhzliH')
    # 得到uid resource_owner_key 和 secret
     #    {u'deviceid': u'0',
     # u'oauth_token': u'824d43c51e4765dfbe214f2fd08ff47cb1f490ef48b02e432b9b01026e7b74c7',
     # u'oauth_token_secret': u'01865c02d51e28f1957ec3193d251b1e6b0b3362996ef49c8b4e9d1071777',
     # u'userid': u'6828098'}