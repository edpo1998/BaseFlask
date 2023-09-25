from .enviroments import conf
from .database import db, migrate
from .json_web_token import jwt

def getPaginateParams(pageNumber: int, pageSize: int):
    if pageNumber == None or pageNumber < 1:
        pageNumber = 1
    if pageSize == None or pageSize < 1:
        pageSize = 10
    return pageNumber, pageSize 