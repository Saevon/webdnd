from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings

from functools import wraps
from webdnd.shared.utils.decorators import cascade
import base64


class ApiError(BaseException):
    ERR_CODE = 000

class InvalidKey(ApiError):
    ERR_CODE = 001

class ApiWarning(BaseException):
    ERR_CODE = 100


class ApiOutput(object):

    def __init__(self):
        self._out = {
            'errors': {
                'num': 0,
                'error': [],
                'warn': [],
            },
            'output': None,
        }

    @cascade
    def error(self, errors):
        """
        Adds a new error to show to the user
        """
        self.problem = False

        if isinstance(errors, list):
            for err in errors:
                self.__error(err)
        else:
            self.__error(errors)

        if self.problem:
            raise ApiError

    def __error(self, err):
        if isinstance(err, ApiWarning):
            self._out['errors']['warn'].append(self.__sanitize_error(err))
        else:
            self._out['errors']['error'].append(self.__sanitize_error(err))
            self._out['errors']['num'] += 1
            self.problem = True

    def __sanitize_error(self, err):
        return {
            'message': unicode(err),
            'code': err.ERR_CODE,
        }

    @cascade
    def output(self, out):
        """
        Sets the output to show the user
        """
        self._out['output'] = out
        if isinstance(out, list):
            # Paging doesn't really work right now
            # And might not
            self._out['paging'] = {
                'page': 1,
                'length': len(out),
                'pagelen': -1,
                'pages': 1,
                'total': len(out),
            }

    def sanitize(self):
        """
        Returns the proper data object to output
        """
        return self._out

def api_output(func):
    """
    Passes in a new ApiOutput to the function every call and catches any problem with the input
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        out = ApiOutput()
        kwargs['output'] = out
        try:
            func(*args, **kwargs)
        except ApiError:
            pass
        return out.sanitize()
    return wrapper



def http_auth_login(func):
    '''
    Allows pre-request login for Api endpoints
    '''
    @wraps(func)
    def view_or_basicauth(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == 'basic':
                username, password = base64.b64decode(auth[1]).split(':')

                # Only allowed a limited subset to use this login method
                # Don't even let the other users know it exists
                if username in settings.HTTP_AUTH_USERS:
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                            login(request, user)
                            request.user = user
                            return func(request, *args, **kwargs)
                else:
                    response = HttpResponse()
                    response.status_code = 403
                    return response

        # No Authorization, err out
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="api"'
        return response
    return view_or_basicauth

