from flask_restx import abort

def order_by(query, object, orderby: str, order: str, defaultOrder: str = None):
    if orderby != None and orderby != '':
        if not hasattr(object, orderby):
            abort(409, 'No es posible ordenar por: "{0}"'.format(orderby))

        if order != None and order != '':
            if order not in ['asc', 'desc']:
                abort(409, 'Ordenamiento incorrecto')
            if order == 'asc':
                query = query.order_by(getattr(object, orderby).asc())
            else:
                query = query.order_by(getattr(object, orderby).desc())
        else:
            query = query.order_by(getattr(object, orderby))
    else:
        if defaultOrder != None:
            if defaultOrder == 'createDate':
                query = query.order_by(getattr(object, defaultOrder).desc())
            else:
                query = query.order_by(getattr(object, defaultOrder))
    return query

def filter(query, object, params, exclude=[]):
    for key in params:
        if params[key] != None and hasattr(object, key) and not key in exclude:
            if type(params[key]) == str:
                query = query.filter(getattr(object, key).ilike('%'+params[key]+'%'))
            else:
                query = query.filter(getattr(object, key) == params[key])
    return query

def listQuery(query, object, params, defaultOrder: str=None, exclude=[]):
    query = filter(query, object, params, exclude)
    query = order_by(query, object, params['orderby'], params['order'], defaultOrder)
    return query