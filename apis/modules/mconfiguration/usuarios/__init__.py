from flask_restx import Namespace, fields, inputs
from apis.models import usuarioModel
from core.utils import paginatorModel
from .. import MODULE_NAME

api = Namespace(f'{MODULE_NAME} - Usuarios')
primaryKey = 'codUsuario'
singleName = 'El Usuario'
pluralName = 'Los Usuarios'

queryParams = {
    'codUsuario': int,
    'createDate': inputs.date_from_iso8601,
    'updateDate': inputs.date_from_iso8601,
    'deleteDate': inputs.date_from_iso8601,
    'userAt': int,
    'activo': inputs.boolean,
    'usuario': str,
    'password': str,
    'nombre': str,
    'apellido': str,
    'correo': str,
}

baseModel = api.inherit('usuarioBaseModel', usuarioModel, {
})

requestBody = api.model('usuarioBodyRequest', {
    'activo': fields.Boolean(required=False),
    'usuario': fields.String(required=True),
    'password': fields.String(required=True),
    'nombre': fields.String(required=True),
    'apellido': fields.String(required=True),
    'correo': fields.String(required=False),
})

pgResponse = api.model('usuarioPgResponse', paginatorModel(baseModel))

from .usuario_resource import UsuarioResource
from .usuarios_resource import UsuariosResource
from .usuarios_pg_resource import UsuariosPgResource
