from flask_restx import Namespace, fields
from .. import moduleName

api = Namespace(f'{moduleName} - Login')

requestBody = api.model('LoginRequest', {
    'usuario': fields.String(example='test', required=True),
    'password': fields.String(example='test', required=True)
})


from .login_resource import LogInResource
from .refresh_token_resource import RefreshTokenResource