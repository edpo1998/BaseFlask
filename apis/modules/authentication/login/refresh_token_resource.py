
from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.database import Usuarios
from core.json_web_token import token_generator
from . import api, requestBody

@api.route('/refresh-token')
class RefreshTokenResource(Resource):

    @jwt_required()
    @api.expect(requestBody)
    def get(self):
        usr: Usuarios = Usuarios.getUserByUsername(get_jwt_identity())
        try:
            token: str = token_generator.generateToken(usr=usr)
            return token, 200
        except Exception as error:
            abort(500, error)