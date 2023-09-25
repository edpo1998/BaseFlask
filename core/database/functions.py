from datetime import datetime
from core.database import db

def setObjValues(objClass, instance, data, userAt: int, omitKeys: list=[], hasCrud: bool=True, isCreate: bool=True, isEdit: bool=False):
    """
        Setea valores a un objeto de base de datos utilizando informacion de un diccionario de datos.

        Args:
            objclass: Clase que se utiliza como molde para setear los datos.
            instance: Instancia de la clase a la que se asigna la información.
            data: Diccionario de datos con la información a setear (Las llaves deben de coincidir
                con los atributos de clase).
            userAt (int): Código del usuario que realiza la transacción.
            omitKeys (list[str]): Listado de las llaves que se deben de omitir en el seteo de valores.
            hasCrud (bool): Si tiene campos CRUD como createDate, updateDate, userAt...
            isCreate (bool): Si se ejecuta para una creacion de objeto.
            isEdit (bool): Si se ejectua para editar un objeto.
    """
    if isCreate and hasCrud:
        instance.createDate = datetime.now()
        instance.userAt = userAt
        instance.activo = True
    
    if isEdit and hasCrud:
        instance.updateDate = datetime.now()
        if 'activo' in data:
            if instance.activo == True and data['activo'] == False:
                instance.deleteDate = datetime.now()
            elif instance.activo == False and data['activo'] == True:
                instance.deleteDate = None

    for key in data:
            if key not in omitKeys and hasattr(objClass, key):
                setattr(instance, key, data[key])
