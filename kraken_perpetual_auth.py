import hashlib
import hmac
import json
import time
import base64
from urllib.parse import urlencode
from decimal import Decimal
from typing import (
    List,
    Mapping,
)

from hummingbot.core.web_assistant.auth import AuthBase
from hummingbot.core.web_assistant.connections.data_types import (
    RESTMethod,
    RESTRequest,
    WSRequest,
)


class KrakenPerpetualAuth(AuthBase):
    """
    Auth class required by Kraken Perpetual API
    Based on https://docs.futures.kraken.com/
    """

    def __init__(self, api_key: str, secret_key: str):
        self._useragent = "cf-api-python/1.0"
        self._api_key: str = api_key
        self._secret_key: str = secret_key

        # Additional Parameters
        self.nonce = 0
        self.checkCertificate = False
        self.useNonce = False

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        if request.method == RESTMethod.GET:
            request = await self._authenticate_get(request)
        elif request.method == RESTMethod.POST:
            request = await self._authenticate_post(request)
        else:
            raise NotImplementedError
        return request

    async def _authenticate_get(self, request: RESTRequest) -> RESTRequest:
        params = request.params or {}
        request.headers = self._create_auth_header(
            request.endpoint_url,
            dict(params),
        )
        return request

    async def _authenticate_post(self, request: RESTRequest) -> RESTRequest:
        params = json.loads(request.data) if request.data is not None else {}
        request.headers = self._create_auth_header(
            request.endpoint_url,
            dict(params),
        )
        data = {key: value for key, value in sorted(params.items())}
        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        This method is intended to configure a websocket request to be authenticated.
        OKX does not use this
        functionality
        """
        return request  # pass-through

    def get_ws_auth_payload(self) -> List[str]:
        """
        Generates a dictionary with all required information for the
        authentication process
        :return: a dictionary of authentication info including the request signature
        """
        expires = self._get_expiration_timestamp()
        raw_signature = "GET/realtime" + expires
        signature = hmac.new(
            self._secret_key.encode("utf-8"),
            raw_signature.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        auth_info = [self._api_key, expires, signature]

        return auth_info

    def _create_auth_header(
        self,
        endpoint_url,
        params: Mapping[str, str],
    ) -> Mapping[str, str]:
        """
        Generate Authent HEADERS for Kraken rest api requests
        :return: a dictionary of authentication info including the request signature
        """
        postData = urlencode(params)
        nonce = self._get_nonce() if self.useNonce else ""
        signature = self._sign_message(
            endpoint_url,
            postData,
            nonce=nonce,
        )

        authentHeaders = {
            "APIKey": self._api_key,
            "Authent": signature,
        }

        if self.useNonce:
            authentHeaders["Nonce"] = nonce

        authentHeaders["User-Agent"] = self._useragent

        return authentHeaders

    def _sign_message(self, endpoint_url, postData, nonce="") -> bytes:
        """
        Utility function for signature generation for AUTH Header
        :return: based64 encoded version of the HMAC Digest
        """
        if endpoint_url.startswith("/derivatives"):
            endpoint_url = endpoint_url[len("/derivatives") :]

        # step 1: concatenate postData, nonce + endpoint
        message = postData + nonce + endpoint_url

        # step 2: hash the result of step 1 with sha256
        sha256_hash = hashlib.sha256()
        sha256_hash.update(message.encode("utf8"))
        hash_digest = sha256_hash.digest()

        # step 3: base64 decode _secret_key
        secretDecoded = base64.b64decode(self._secret_key)

        # step 4: use result of setp 3 to hash the result of step 2 with HMAC-SHA512
        hmac_digest = hmac.new(secretDecoded, hash_digest, hashlib.sha512).digest()

        # step 5: base64 encode the result of step 4 and return
        return base64.b64decode(hmac_digest)

    def _get_nonce(self):
        self.nonce = (self.nonce + 1) & 8191
        return str(int(time.time() * 1000)) + str(self.nonce).zfill(4)

    @staticmethod
    def _get_timestamp():
        return str(int(time.time() * 1e3))

    @staticmethod
    def _get_expiration_timestamp():
        return str(int((round(time.time()) + 5) * 1e3))
