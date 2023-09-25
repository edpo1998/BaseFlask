from flask_restx import Resource, abort
from core import conf
from core.database import db, Usuarios
from flask_jwt_extended import jwt_required, get_jwt_identity
from cryptography.fernet import Fernet
from . import api, requestBody

@api.route('')
class PaswordChangeResource(Resource):

    @jwt_required()
    @api.expect(requestBody)
    def post(self):
        data = api.payload
        userName = str(get_jwt_identity())
        user = Usuarios.getUserByUsername(userName)
        f = Fernet(conf.CRYPTO_SECRET_KEY)

        if f.decrypt(user.password.encode()).decode() != data['oldPassword']:
            abort(401, 'Contraseña incorrecta')

        criptPass = f.encrypt(str(data['newPassword']).encode())
        user.password = criptPass.decode()

        try:
            db.session.commit()
        except:
            abort(500, 'Error al guardar la información')