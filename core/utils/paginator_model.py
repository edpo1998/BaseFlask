from flask_restx import fields

def paginatorModel(baseModel):
    return {
        'total': fields.Integer,
        'page': fields.Integer,
        'pages': fields.Integer,
        'items': fields.List(fields.Nested(baseModel))
    }