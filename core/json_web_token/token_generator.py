import datetime
from flask_jwt_extended import create_access_token
from core.database import Usuarios
from core import conf

def generateToken(usr: Usuarios):
    """ Funcion para generar el Token
        Params
        -------
        usr: Usuarios
            instancia orm  que identifica al usuario a logear
    """
    try:
        deltaTime = datetime.timedelta(minutes=int(conf.LOGIN_EXPIRE_TIME))
        claims = { 
            'fullname': '{0} {1}'.format(usr.nombre, usr.apellido),
            'name': usr.nombre,
            'lastname': usr.apellido,
        }
        token = create_access_token(identity=usr.usuario, expires_delta=deltaTime, additional_claims=claims)
        return token
    except Exception as e:
        raise ValueError("Error al crear token")