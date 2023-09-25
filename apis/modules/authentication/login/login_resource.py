from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from cryptography.fernet import Fernet
from core import conf
from core.database import db, Usuarios
from core.json_web_token import token_generator
from . import api, requestBody
@api.route('')
class LogInResource(Resource):

    @jwt_required()
    def get(self):
        usr: Usuarios = db.session.query(Usuarios).get(int(get_jwt_identity()))
        if usr is None:
            abort(401, 'El usuario no existe')

        try:
            token = token_generator.generateToken(usr=usr)
            return token
        except Exception as error:
            abort(500, error)
  
    @api.expect(requestBody)
    def post(self):
        user = str(api.payload['usuario'])
        pssw = str(api.payload['password'])

        usr: Usuarios = db.session.query(Usuarios).filter(Usuarios.usuario == user).first()
        if usr is None:
            abort(401, 'Usuario incorrecto')

        if not usr.activo:
            abort(401, 'Usuario inactivo')
        
        f = Fernet(conf.CRYPTO_SECRET_KEY)

        passwordVerify = lambda pss: f.decrypt(usr.password.encode()).decode() == api.payload['password']
        if not passwordVerify(pssw):
            abort(401, 'Contraseña incorrecta')

        try:
            token: str = token_generator.generateToken(usr=usr)
            return token, 200
        except Exception as error:
            abort(500, error)