from flask_restx import Resource, abort
from core.database import db, Usuarios, Usuarios, setObjValues
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from . import api, baseModel, requestBody
from . import primaryKey, singleName

@api.route('/<int:id>')
class UsuarioResource(Resource):

    @jwt_required()
    @api.marshal_with(baseModel)
    def get(self, id):
        try:
            item: Usuarios = db.session.query(Usuarios).get(id)
        except:
            abort(500, 'Error al obtener {0}'.format(singleName))
        if item is None:
            abort(404, '{0} no existe'.format(singleName.capitalize()))
        return item

    @jwt_required()
    @api.expect(requestBody, validate=True)
    @api.marshal_with(baseModel)
    def put(self, id):
        data = api.payload
        try:
            updateItem: Usuarios = db.session.query(Usuarios).get(id)
            itemState = updateItem.activo
            usr: Usuarios = Usuarios.getUserByUsername(get_jwt_identity())
        except:
            abort(500, 'Error al obtener {0}'.format(singleName))

        if usr is None:
            abort(404, 'Usuario no valido')

        if updateItem is None:
            abort(404, '{0} no existe'.format(singleName.capitalize()))

        setObjValues(Usuarios, updateItem, data, usr.codUsuario, [primaryKey], isCreate=False, isEdit=True)
        try:
            db.session.commit()
            return updateItem
        except:
            abort(500, 'Error al actualizar {0}'.format(singleName))

    @jwt_required()
    @api.expect(requestBody)
    @api.marshal_with(baseModel)
    def patch(self, id):
        data = api.payload
        try:
            updateItem: Usuarios = db.session.query(Usuarios).get(id)
            itemState = updateItem.activo
            usr: Usuarios = Usuarios.getUserByUsername(get_jwt_identity())
        except:
            abort(500, 'Error al obtener informacion')

        if updateItem is None:
            abort(404, '{0} no existe'.format(singleName.capitalize()))

        setObjValues(Usuarios, updateItem, data, usr.codUsuario, [primaryKey], isCreate=False, isEdit=True)
        try:
            db.session.commit()
            return updateItem
        except:
            abort(500, 'Error al actualizar {0}'.format(singleName))
