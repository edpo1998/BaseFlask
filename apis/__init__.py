from flask_restx import Api

authorizations = {
    'token': {"type": "apiKey", "name": "Authorization", "in": "header"}
}

api = Api(
    title='Core API',
    version='1.0',
    description='API Base',
    authorizations=authorizations,
    security='token',
    ordered=True
)

api.prefix = '/api/v1'

from .models import *
from .modules import *

# Authentication
api.add_namespace(login, '/authentication/login')
api.add_namespace(passwordChange, '/authentication/password-change')

# Configuration
api.add_namespace(usuarios, '/mconfiguration/usuarios')



