import os
import re

import requests


class PyAqError(Exception):
    """ Generic exception for Trident request errors """


class Requestor(object):
    """ Wraps a function to raise error with unexpected request status codes """

    def __init__(self, status_codes):
        if not isinstance(status_codes, list):
            status_codes = [status_codes]
        self.code = status_codes

    def __call__(self, f):
        def wrapped_f(s, path, *args, **kwargs):
            # add headers
            k = {"headers": s.headers}
            k.update(kwargs)

            # update path
            args = list(args)
            path = os.path.join(s.home, path)
            r = f(s, path, *args, **k)

            # check status codes
            if r.status_code not in self.code:
                http_codes = {
                    403: "FORBIDDEN",
                    404: "NOT FOUND",
                    500: "INTERNAL SERVER ERROR",
                    503: "SERVICE UNAVAILABLE",
                    422: "UNPROCESSABLE UNTITY. Your login information may be incorrect or db item does not exist.",
                    504: "SERVER TIMEOUT"}
                msg = ""
                if r.status_code in http_codes:
                    msg = http_codes[r.status_code]
                    msg += "\npath: {0}\nheaders: {1}\ndata: {2}".format(path, s.headers, k)
                    msg += "\n{0}".format(r.json())
                raise PyAqError("HTTP Response Failed {} {}".format(
                        r.status_code, msg))
            return r

        return wrapped_f


class AqHTTP(object):
    """ Methods for API """
    def __init__(self, login, password, home):
        self.login = login
        self.password = password
        self.home = home
        self.headers = {}
        self._login()

    def _create_session(self):
        return {
            "session": {
                "login"   : self.login,
                "password": self.password
            }
        }

    def _login(self):
        r = self._post("sessions.json", json=self._create_session())
        self._save_cookie(r)

    def _save_cookie(self, r):
        self.headers = {
            "cookie": AqHTTP.__fix_remember_token(
                    r.headers["set-cookie"]
            )
        }

    @Requestor([200])
    def _post(self, path, json=None, **kwargs):
        return requests.post(path, json=json, **kwargs)

    @Requestor
    def _put(self, path, json=None, **kwargs):
        return requests.put(path, json=json, **kwargs)

    @Requestor
    def _get(self, path, **kwargs):
        return requests.get(path, **kwargs)

    @staticmethod
    def __fix_remember_token(h):
        parts = h.split(';')
        rtok = ""
        for c in parts:
            cparts = c.split('=')
            if re.match('remember_token', cparts[0]):
                rtok = cparts[1]
        return "remember_token="+rtok+"; "+h


class Session:
    """ Creates api sessions """
    session = None
    login = None
    password = None
    url = None

    @classmethod
    def create(cls, login, password, url):
        cls.login = login
        cls.password = password
        cls.url = url
        cls.new()

    @classmethod
    def new(cls):
        cls.session = AqHTTP(login=cls.login, password=cls.password, home=cls.url)
