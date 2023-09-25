from pprint import pprint
import re, os
from utils import spinalToCamel, toSingularWord, createFolder
from colorama import Fore

class Column():
    def __init__(self, dbName:str, name: str, dataType: str, nullable: bool=False, isPrimaryKey: bool=False, reference: str=None, isIncrement: bool=False):
        self.dbName = dbName
        self.name = name
        self.dataType = dataType
        self.nullable = nullable
        self.isPrimaryKey = isPrimaryKey
        self.reference = reference
        self.isIncrement = isIncrement

class Table():
    def __init__(self, schema: str, name: str):
        self.schema = schema
        self.name = name
        self.className = spinalToCamel(name, True)
        self.columns: list[Column] = []
        self.sqlLines: list[str] = []
    
    def addColumn(self, column: Column):
        self.columns.append(column)
    
    def addSqlLine(self, line: str):
        self.sqlLines.append(line)

def formatDocumentLines(inputLines: list[str]):
    outputLines = []
    for line in inputLines:
        formatedLine = line.replace('\n', '').replace('  ', ' ').strip().rstrip(',')
        if formatedLine not in ['(', ');', '']:
            outputLines.append(formatedLine)
    return outputLines

def getTablesObj(docLines: list[str]):
    output: list[Table] = []

    tables: list[list[str]] = []
    index: int = -1
    for line in docLines:
        if re.search('create table', line.lower()):
            index += 1
            tables.append([])
        if index >= 0:
            tables[index].append(line)
    
    for tableLines in tables:
        lineaCero: str = tableLines.pop(0)
        schemaName, tableName = getTableSN(lineaCero)
        table = Table(schemaName, tableName)
        table.sqlLines.append(lineaCero)
        for colLine in tableLines:
            table.addSqlLine(colLine)
            colDbName = colLine.split(' ')[0]
            colName = spinalToCamel(colDbName)
            column = Column(
                colDbName,
                colName,
                getDataType(colName, colLine),
                isNullable(colLine),
                isPrimaryKey(colLine),
                getReferences(colLine),
                isIncrement(colLine)
            )
            table.addColumn(column)
        output.append(table)
    return output

def getTableSN(txt: str):
    if re.search('create table', txt.lower()):
        partes = txt.split('.')
        schema: str = partes[0].split(' ')[-1]
        table: str = partes[1].strip()
        return schema, table
    else:
        print(Fore.RED, f'* Error al obtener el esquema y nombre de la tabla. "{txt}"', Fore.RESET)
        exit()

def getDataType(colName: str, line: str):
    line = line.lower()
    if re.search('smallserial|smallint', line):
        return 'db.SmallInteger'
    if re.search('bigserial|bigint', line):
        return 'db.BigInteger'
    if re.search('serial|integer', line):
        return 'db.Integer'
    if re.search('numeric\(.*\)', line):
        value = re.search('\(.*\)', line)
        return f'db.Numeric{value.group()}'
    if re.search('timestamp\(.*\)', line):
        return 'TIMESTAMP(False, 0)'
    if re.search('boolean', line):
        return 'db.Boolean'
    if re.search('varchar|character|char|(character varying)', line):
        value = re.search('\(.*\)', line)
        if value != None:
            return f'db.String{value.group()}'
        else:
            return 'db.String'
    print(Fore.RED, f'* No fue posible obtener el tipo de dato para la columna {colName}', Fore.RESET)
    exit()

def isIncrement(line: str):
    line = line.lower()
    if re.search('smallserial|serial|bigserial', line):
        return True
    else:
        return False

def isPrimaryKey(line: str):
    if re.search('PRIMARY KEY', line):
        return True
    else:
        return False

def isNullable(line: str):
    if re.search('NOT NULL', line) or isPrimaryKey(line): return False
    else: return True

def isForeignKey(line: str):
    if re.search('REFERENCES', line): return True
    else: return False

def getReferences(line: str):
    if isForeignKey(line):
        reference = line.split(' ')[-1]
        split = reference.split('.')
        schema = split[0]
        table = split[1]
        temp = table.split('_')
        idWords = ['cod']
        for word in temp:
            idWords.append(toSingularWord(word))
        id = '_'.join(idWords)
        return f'\'{schema}.{table}.{id}\''
    else: return None

def generateTableFiles(table: Table):
    f = open(f'core/database/{table.schema}_schema/{table.name}.py', 'w')
    f.writelines([
        'from core.database import db, query_functions\n',
        'from sqlalchemy.dialects.postgresql import TIMESTAMP\n'
        'from . import schema_name\n',
        f'\nclass {table.className}(db.Model):',
        f'\n    __tablename__ = \'{table.name}\'',
        '\n    __table_args__ = {\'schema\':schema_name}\n\n'
    ])

    for col in table.columns:
        colWriter = f'    {col.name} = db.Column(\'{col.dbName}\', {col.dataType}'
        if col.reference != None:
            colWriter += f', db.ForeignKey({col.reference})'
        colWriter += f', nullable={col.nullable}'
        if col.isPrimaryKey == True: colWriter += ', primary_key=True'
        if col.isPrimaryKey == True and col.dataType in ['db.SmallInteger', 'db.Integer', 'db.BigInteger']:
            if col.isIncrement: colWriter += ', autoincrement=True'
            else: colWriter += ', autoincrement=False'

        f.write(colWriter + ')\n')

    f.writelines([
        '\n\n    def listQuery(params):',
        f'\n        query = db.session.query({table.className})',
        f'\n        query = query_functions.listQuery(query, {table.className}, params, \'createDate\')',
        f'\n        return query \n\n'
    ])

    f.write('\n# ' + table.sqlLines[0] + '\n# (')
    f.writelines(f'\n#     {l},' for l in table.sqlLines[1:-1])
    f.write(f'\n#     {table.sqlLines[-1]}')
    f.write('\n# );')
            
    f.close()

def importarInit(schema: str, table: str, className: str):
    createFolder(f'core/database/{schema}_schema')
    existInit = os.path.exists(f'core/database/{schema}_schema/__init__.py')
    init = open(f'core/database/{schema}_schema/__init__.py', 'a')
    if existInit == False:
        init.write(f"schema_name = '{schema}'\n")
    init.write(f"\nfrom .{table} import {className}")
    init.close()

### INICIO DE EJECUCION ###

importInit = input('¿Realizar importaciones a init.py? [y/n] ')
with open('core/utils/scaffold/sql_input.sql') as input:
    lines = formatDocumentLines(input.readlines())
    tables: list[Table] = getTablesObj(lines)
    for table in tables:
        if importInit == 'y':
            importarInit(table.schema, table.name, table.className)
        generateTableFiles(table)
    
    print(Fore.CYAN, '* Scaffold realizado con exito', Fore.RESET)