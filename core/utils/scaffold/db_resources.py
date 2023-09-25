from utils import camelCaseSplit, toSingularWord, firstLower, getColumnDataType, isNotNullCol, getPrimarykey, spinalToCamel, createFolder, getSwaggerName
import re
from colorama import Fore

def getTableInfo(schema: str, table: str):
    with open(f'core/database/{schema}_schema/{table}.py') as table:
        tableLines = table.readlines()
        columns = {}
        className = None
        for line in tableLines:
            formatLine = line.replace('\n', '').replace('    ', '')
            if re.search('class', formatLine):
                className = formatLine.split(' ')[1]
                className = className.split('(')[0]
            if re.search('db.Column', formatLine):
                colName: str = formatLine.split(' ')[0]
                isPrimaryKey: bool = True if re.search('primary_key=True', formatLine) else False
                colFieldType, colInputType = getColumnDataType(formatLine)
                if colFieldType == None or colInputType == None:
                    print(Fore.RED, f'* No fue posible obtener el tipo de dato para la columna {colName}', Fore.RESET)
                    exit()
                columns[colName] = {
                    'primaryKey': isPrimaryKey,
                    'notNull': isNotNullCol(formatLine),
                    'field': colFieldType,
                    'input': colInputType
                }
        
        return className, columns

def addModel(className: str, dataDictionary: dict):
    modelName = ''.join([toSingularWord(word) for word in camelCaseSplit(className)])
    variableName = firstLower(modelName)
    f = open(f'apis/models/{schema}.py', 'a')
    f.write(f"\n\n{variableName}Model = api.model('{modelName}', {{\n")
    for key in dataDictionary:
        f.write(f"    '{key}': {dataDictionary[key]['field']},\n")
    f.write('})')
    f.close()

def createInit(schema: str, table: str, className: str, fieldsDict: dict):
    modelName = ''.join([toSingularWord(word) for word in camelCaseSplit(className)])
    variableName = firstLower(modelName)
    f = open(f'apis/modules/{schema}/{table}/__init__.py', 'w')
    swaggerName = getSwaggerName(table)
    singleName = input('Nombre en singular (Mensajes): ')
    pluralName = input('Nombre en plural (Mensajes): ')
    primaryKey = getPrimarykey(fieldsDict)
    f.writelines([
        'from flask_restx import Namespace, fields, inputs\n',
        f'from apis.models import {variableName}Model\n'
        f'from core.utils import paginatorModel\n',
        f'from .. import MODULE_NAME\n\n',
        f"api = Namespace(f'{{MODULE_NAME}} - {swaggerName}')\n",
        f"primaryKey = '{primaryKey}'\n",
        f"singleName = '{singleName}'\n",
        f"pluralName = '{pluralName}'\n\n",
    ])

    # queryParams
    f.write(f"queryParams = {{\n")
    for key in fieldsDict:
        f.write(f"    '{key}': {fieldsDict[key]['input']},\n")
    f.write('}\n\n')

    # baseModel
    f.writelines([
        f"baseModel = api.inherit('{variableName}BaseModel', {variableName}Model, {{\n",
        "})\n\n"
    ])

    # requestBody
    f.write(f"requestBody = api.model('{variableName}BodyRequest', {{\n")
    for key in fieldsDict:
        if key not in [primaryKey, 'createDate', 'updateDate', 'deleteDate', 'userAt']:
            f.write(f"    '{key}': {fieldsDict[key]['field']}(required={fieldsDict[key]['notNull'] and key != 'activo'}),\n")
    f.write('})\n\n')

    # pgResponse
    f.write(f"pgResponse = api.model('{variableName}PgResponse', paginatorModel(baseModel))\n\n")

    # importaciones
    tableSplit = table.split('_')
    singularResourceName = '_'.join([toSingularWord(word) for word in tableSplit])
    f.writelines([
        f"from .{singularResourceName}_resource import {spinalToCamel(singularResourceName, True)}Resource\n",
        f"from .{table}_resource import {className}Resource\n",
        f"from .{table}_pg_resource import {className}PgResource\n",
    ])

    f.close()
    
def createSingleResource(className: str, table: str):
    tableSplit = table.split('_')
    singularResourceName = '_'.join([toSingularWord(word) for word in tableSplit])
    f = open(f'apis/modules/{schema}/{table}/{singularResourceName}_resource.py', 'x')
    f.writelines([
        "from flask_restx import Resource, abort\n",
        f"from core.database import db, Usuarios, {className}, setObjValues\n",
        "from flask_jwt_extended import jwt_required, get_jwt_identity\n",
        "from datetime import datetime\n\n",
        "from . import api, baseModel, requestBody\n",
        "from . import primaryKey, singleName\n\n",
        "@api.route('/<int:id>')\n",
        f"class {spinalToCamel(singularResourceName, True)}Resource(Resource):\n\n",
        "    @jwt_required()\n",
        "    @api.marshal_with(baseModel)\n",
        "    def get(self, id):\n",
        "        try:\n",
        f"            item: {className} = db.session.query({className}).get(id)\n",
        "        except:\n",
        "            abort(500, 'Error al obtener {0}'.format(singleName))\n",
        "        if item is None:\n",
        "            abort(404, '{0} no existe'.format(singleName.capitalize()))\n",
        "        return item\n\n",

        "    @jwt_required()\n",
        "    @api.expect(requestBody, validate=True)\n",
        "    @api.marshal_with(baseModel)\n",
        "    def put(self, id):\n",
        "        data = api.payload\n",
        "        try:\n",
        f"            updateItem: {className} = db.session.query({className}).get(id)\n",
        "            itemState = updateItem.activo\n",
        "            usr: Usuarios = Usuarios.getUserByUsername(get_jwt_identity())\n",
        "        except:\n",
        "            abort(500, 'Error al obtener {0}'.format(singleName))\n\n",
        "        if usr is None:\n",
        "            abort(404, 'Usuario no valido')\n\n",
        "        if updateItem is None:\n",
        "            abort(404, '{0} no existe'.format(singleName.capitalize()))\n\n",
        f"        setObjValues({className}, updateItem, data, usr.codUsuario, [primaryKey], isCreate=False, isEdit=True)\n",
        "        try:\n",
        "            db.session.commit()\n",
        "            return updateItem\n",
        "        except:\n",
        "            abort(500, 'Error al actualizar {0}'.format(singleName))\n\n",

        "    @jwt_required()\n",
        "    @api.expect(requestBody)\n",
        "    @api.marshal_with(baseModel)\n",
        "    def patch(self, id):\n",
        "        data = api.payload\n",
        "        try:\n",
        f"            updateItem: {className} = db.session.query({className}).get(id)\n",
        "            itemState = updateItem.activo\n"
        "            usr: Usuarios = Usuarios.getUserByUsername(get_jwt_identity())\n"
        "        except:\n",
        "            abort(500, 'Error al obtener informacion')\n\n",
        "        if updateItem is None:\n",
        "            abort(404, '{0} no existe'.format(singleName.capitalize()))\n\n",
        f"        setObjValues({className}, updateItem, data, usr.codUsuario, [primaryKey], isCreate=False, isEdit=True)\n",
        "        try:\n",
        "            db.session.commit()\n",
        "            return updateItem\n",
        "        except:\n",
        "            abort(500, 'Error al actualizar {0}'.format(singleName))\n",
    ])
    f.close()

def createPluralResource(className: str, table: str):
    f = open(f'apis/modules/{schema}/{table}/{table}_resource.py', 'x')
    f.writelines([
        "from flask_restx import Resource, abort\n",
        f"from core.database import db, Usuarios, {className}, setObjValues\n",
        "from flask_jwt_extended import jwt_required, get_jwt_identity\n",
        "from datetime import datetime\n",
        "from core.utils import argument_parser as ap\n\n",
        "from . import api, queryParams, baseModel, requestBody\n",
        "from . import primaryKey, pluralName, singleName\n\n",
        "@api.route('')\n",
        f"class {className}Resource(Resource):\n\n",
        "    parser = api.parser()\n",
        "    parser = ap.addArguments(queryParams, parser)\n\n",
        "    @jwt_required()\n",
        "    @api.expect(parser)\n",
        "    @api.marshal_list_with(baseModel)\n",
        "    def get(self):\n",
        "        args = self.parser.parse_args()\n",
        f"        query = {className}.listQuery(args)\n",
        "        try:\n",
        "            return query.all()\n",
        "        except:\n",
        "            abort(500, 'Error al obtener {0}'.format(pluralName))\n\n",
        "    @jwt_required()\n",
        "    @api.expect(requestBody, validate=True)\n",
        "    @api.marshal_with(baseModel)\n",
        "    def post(self):\n",
        "        data = api.payload\n",
        "        usr: Usuarios = Usuarios.getUserByUsername(get_jwt_identity())\n\n",
        f"        newItem = {className}()\n",
        f"        setObjValues({className}, newItem, data, usr.codUsuario, [primaryKey])\n",
        "        db.session.add(newItem)\n",
        "        try:\n",
        "            db.session.commit()\n",
        "            return newItem\n",
        "        except:\n",
        "            abort(500, 'Error al crear {0}'.format(singleName))\n",
    ])
    f.close()

def createPaginateResource(className: str, table: str):
    f = open(f'apis/modules/{schema}/{table}/{table}_pg_resource.py', 'x')
    f.writelines([
        "from flask_restx import Resource, abort, inputs\n",
        f"from core.database import {className}\n",
        "from flask_jwt_extended import jwt_required\n",
        "from core import getPaginateParams\n",
        "from core.utils import argument_parser as ap\n\n",
        "from . import api, queryParams, pgResponse\n",
        "from . import pluralName\n\n",
        "@api.route('/pg')\n",
        f"class {className}PgResource(Resource):\n",
        "    parser = api.parser()\n",
        "    parser = ap.addArguments(queryParams, parser, True)\n\n",
        "    @jwt_required()\n",
        "    @api.expect(parser)\n",
        "    @api.marshal_with(pgResponse)\n",
        "    def get(self):\n",
        "        args = self.parser.parse_args()\n",
        "        page, size = getPaginateParams(args['page'], args['pageSize'])\n",
        f"        query = {className}.listQuery(args)\n",
        "        try:\n",
        "            return query.paginate(page=page, per_page=size)\n",
        "        except:\n",
        "            abort(500, 'Error al obtener {0}'.format(pluralName))\n",
    ])
    f.close()

def importarRecurso(className: str, table: str):
    f = open(f'apis/modules/{schema}/__init__.py', 'a')
    f.write(f'\nfrom .{table} import api as {firstLower(className)}')
    f.close()

schema = input('Esquema: ').lower()
table = input('Tabla (nombre de la tabla): ').lower()
className, fieldsDict = getTableInfo(schema, table)
createFolder(f'apis/modules/{schema}/{table}')
addModel(className, fieldsDict)
createInit(schema, table, className, fieldsDict)
createSingleResource(className, table)
createPluralResource(className, table)
createPaginateResource(className, table)
importarRecurso(className, table)
print(Fore.CYAN, '* Scaffold realizado con exito', Fore.RESET)