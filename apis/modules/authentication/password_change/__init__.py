from flask_restx import Namespace, fields
from .. import moduleName

api = Namespace(f'{moduleName} - Password Change')

requestBody = api.model('passwordChangeRequest', {
    'oldPassword': fields.String,
    'newPassword': fields.String
})

from .password_change_resource import PaswordChangeResource
