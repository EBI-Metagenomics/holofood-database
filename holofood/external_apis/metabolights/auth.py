from requests.auth import AuthBase

from holofood.utils import holofood_config


class UserTokenAuth(AuthBase):
    def __init__(self, user_token):
        self.user_token = user_token

    def __eq__(self, other):
        return all(
            [
                self.user_token == getattr(other, "user_token", None),
            ]
        )

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers["User_token"] = self.user_token
        return r


if holofood_config.metabolights.user_token:
    MTBLS_AUTH = UserTokenAuth(holofood_config.metabolights.user_token)
else:
    MTBLS_AUTH = None
