# vim:fileencoding=utf-8:sw=4

import ujson as json

class AWIPError(Exception):
    def todict(self):
        d = {
            'status': 'error',
            'message': str(self),
        }
        return d

class AWIPErrorWithCode(AWIPError):
    code = 599
    msg = 'Error'

    def __init__(self, msg=None, code=None):
        if msg is not None:
            self.msg = msg
        if code is not None:
            self.code = code

    def __str__(self):
        return '%d %s' % (self.code, self.msg)

    def __repr__(self):
        return '<%s:code=%d, msg=%s' % (self.__class__.__name__, self.code, self.msg)

    def todict(self):
        d = {
            'status': 'error',
            'code': self.code,
            'message': self.msg,
        }
        return d


class AWIPClientError(AWIPErrorWithCode):
    code = 400

class AWIPHandshakeFailed(AWIPClientError):
    msg = 'Bad Protocol'
    def __init__(self, initial, *args, **kwargs):
        self.initial = initial
        super(self.__class__, self).__init__(*args, **kwargs)

class AWIPClientDisconnected(AWIPError):
    def __str__(self):
        if not self.args:
            return 'client disconnected'
        else:
            return AWIPError.__str__(self)

class AWIPRequestInvalid(AWIPClientError): pass

class AWIPServerError(AWIPErrorWithCode):
    code = 500

class AWIPOperationError(AWIPErrorWithCode):
    code = 400

