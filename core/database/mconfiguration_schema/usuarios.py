from core.database import db, query_functions
from sqlalchemy.dialects.postgresql import TIMESTAMP

from . import schema_name

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'schema':schema_name}

    codUsuario = db.Column('cod_usuario', db.SmallInteger, nullable=False, primary_key=True, autoincrement=True)
    createDate = db.Column('create_date', TIMESTAMP(False, 0), nullable=False)
    updateDate = db.Column('update_date', TIMESTAMP(False, 0), nullable=True)
    deleteDate = db.Column('delete_date', TIMESTAMP(False, 0), nullable=True)
    userAt = db.Column('user_at', db.SmallInteger, nullable=False)
    activo = db.Column('activo', db.Boolean, nullable=False)
    usuario = db.Column('usuario', db.String(50), nullable=False)
    password = db.Column('password', db.String(101), nullable=False)
    nombre = db.Column('nombre', db.String(50), nullable=False)
    apellido = db.Column('apellido', db.String(50), nullable=False)
    correo = db.Column('correo', db.String(50), nullable=True)

    def listQuery(params):
        query = db.session.query(Usuarios)
        query = query_functions.listQuery(query, Usuarios, params, 'usuario')
        return query

    def getUserByUsername(username: str):
        try:
            user = db.session.query(Usuarios).filter(Usuarios.usuario == username).first()
            if user is None:
                raise ValueError('El usuario no existe')
            return user
        except:
            raise ValueError('Error al obtener el usuario')