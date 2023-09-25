from flask_restx.reqparse import RequestParser

def addArguments(params: dict, parser: RequestParser, isPaginated: bool=False, addOrdenArguments: bool=True):
    if isPaginated == True:
        parser = addPaginatedArguments(parser)

    for param in params:
        parser.add_argument(param, type=params[param], location='args')
    
    if addOrdenArguments:
        parser = addOrderArguments(parser)
    return parser

def addPaginatedArguments(parser: RequestParser):
    parser.add_argument('page', type=int, location='args')
    parser.add_argument('pageSize', type=int, location='args')
    return parser

def addOrderArguments(parser: RequestParser):
    parser.add_argument('orderby', type=str, location='args')
    parser.add_argument('order', type=str, location='args')
    return parser