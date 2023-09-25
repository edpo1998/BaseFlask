from flask_restx import Resource, abort
from core.database import db, Usuarios, Usuarios, setObjValues
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from core.utils import argument_parser as ap

from . import api, queryParams, baseModel, requestBody
from . import primaryKey, pluralName, singleName

@api.route('')
class UsuariosResource(Resource):

    parser = api.parser()
    parser = ap.addArguments(queryParams, parser)

    @jwt_required()
    @api.expect(parser)
    @api.marshal_list_with(baseModel)
    def get(self):
        args = self.parser.parse_args()
        query = Usuarios.listQuery(args)
        try:
            return query.all()
        except:
            abort(500, 'Error al obtener {0}'.format(pluralName))

    @jwt_required()
    @api.expect(requestBody, validate=True)
    @api.marshal_with(baseModel)
    def post(self):
        data = api.payload
        usr: Usuarios = Usuarios.getUserByUsername(get_jwt_identity())

        newItem = Usuarios()
        setObjValues(Usuarios, newItem, data, usr.codUsuario, [primaryKey])
        db.session.add(newItem)
        try:
            db.session.commit()
            return newItem
        except:
            abort(500, 'Error al crear {0}'.format(singleName))
