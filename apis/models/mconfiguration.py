from apis import api
from flask_restx import fields

usuarioModel = api.model('Usuario', {
    'codUsuario': fields.Integer,
    'createDate': fields.DateTime,
    'updateDate': fields.DateTime,
    'deleteDate': fields.DateTime,
    'userAt': fields.Integer,
    'activo': fields.Boolean,
    'usuario': fields.String,
    'password': fields.String,
    'nombre': fields.String,
    'apellido': fields.String,
    'correo': fields.String,
})