from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

db = SQLAlchemy(metadata=MetaData(naming_convention={
    'pk': '%(table_name)s_pkey',
    'fk': '%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fkey',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
}))

migrate = Migrate()

from .mconfiguration_schema import *

from .functions import setObjValues