from .base_transport import BaseTransport
import requests
import json


class HTTP_Transport(BaseTransport):
    def __init__(self, bondid, hostname, port, token):
        self.bondid = bondid
        self._hostname = hostname
        self._port = port
        self._token = token
        self._token_in_header = True
        self._token_in_body = False

    def get(self, topic="", body=None, uuid=None, timeout=None):
        body = {} if body is None else body
        return self.request(requests.get, topic, body, uuid, timeout)

    def post(self, topic="", body=None, uuid=None, timeout=None):
        body = {} if body is None else body
        return self.request(requests.post, topic, body, uuid, timeout)

    def put(self, topic="", body=None, uuid=None, timeout=None):
        body = {} if body is None else body
        return self.request(requests.put, topic, body, uuid, timeout)

    def delete(self, topic="", body=None, uuid=None, timeout=None):
        body = {} if body is None else body
        return self.request(requests.delete, topic, body, uuid, timeout)

    def patch(self, topic="", body=None, uuid=None, timeout=None):
        body = {} if body is None else body
        return self.request(requests.patch, topic, body, uuid, timeout)

    def request(self, method=None, topic="", body=None, uuid=None, timeout=None):
        url = "http://" + self._hostname + ":" + str(self._port) + "/v2/" + topic
        headers = {}
        if timeout is None:
            timeout = 2
        if body is None:
            body = {}
        if self._token_in_body:
            body["_token"] = self._token
        if self._token_in_header:
            headers = {"BOND-Token": self._token}
        if not (uuid is None):
            headers["BOND-UUID"] = uuid
        r = method(url, data=json.dumps(body), headers=headers, timeout=timeout)
        # TODO: add other fields like i, f, and t
        try:
            body = json.loads(r.text)
        except:
            body = None
        rsp = {"s": r.status_code, "b": body, "bondid": self.bondid}
        return rsp
