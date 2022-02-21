import json

import requests

from bond.proto.base_transport import BaseTransport


class HTTP_Transport(BaseTransport):
    def __init__(self, bondid, hostname, port, token):
        self.bondid = bondid
        self._token = token
        self._token_in_header = True
        self._token_in_body = False
        self.root_url = f"http://{hostname}:{port}/v2/"

    def get(self, **kwargs):
        return self.request(requests.get, **kwargs)

    def post(self, **kwargs):
        return self.request(requests.post, **kwargs)

    def put(self, **kwargs):
        return self.request(requests.put, **kwargs)

    def patch(self, **kwargs):
        return self.request(requests.patch, **kwargs)

    def delete(self, **kwargs):
        return self.request(requests.delete, **kwargs)

    def request(self, method, topic="", body=None, uuid=None, timeout=2):
        headers = {}
        if body is None:
            body = {}
        if self._token_in_body:
            body["_token"] = self._token
        if self._token_in_header:
            headers["BOND-Token"] = self._token
        if uuid is not None:
            headers["BOND-UUID"] = uuid
        rsp = method(
            self.root_url + topic,
            data=json.dumps(body),
            headers=headers,
            timeout=timeout,
        )
        # TODO: add other fields like i, f, and t
        try:
            body = json.loads(rsp.text)
        except:  # noqa: E722 - ignore bare except
            body = None
        if rsp.status_code == 401:
            raise PermissionError("Invalid token! Have you set it with 'bond token' yet?")
        return {"s": rsp.status_code, "b": body, "bondid": self.bondid}
