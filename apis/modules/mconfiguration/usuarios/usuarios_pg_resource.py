from flask_restx import Resource, abort, inputs
from core.database import Usuarios
from flask_jwt_extended import jwt_required
from core import getPaginateParams
from core.utils import argument_parser as ap

from . import api, queryParams, pgResponse
from . import pluralName

@api.route('/pg')
class UsuariosPgResource(Resource):
    parser = api.parser()
    parser = ap.addArguments(queryParams, parser, True)

    @jwt_required()
    @api.expect(parser)
    @api.marshal_with(pgResponse)
    def get(self):
        args = self.parser.parse_args()
        page, size = getPaginateParams(args['page'], args['pageSize'])
        query = Usuarios.listQuery(args)
        try:
            return query.paginate(page=page, per_page=size)
        except:
            abort(500, 'Error al obtener {0}'.format(pluralName))
