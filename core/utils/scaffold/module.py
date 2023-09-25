import os
from utils import createFolder

def createInit(schema: str):
    f = open(f'apis/modules/{schema}/__init__.py', 'x')
    f.writelines([
        f"MODULE_NAME = '{schema.upper()}'\n\n"
    ])
    f.close()

def importModule(schema: str):
    f = open(f'apis/modules/__init__.py', 'a')
    f.write(f'\nfrom .{schema} import *')
    f.close()

schema: str = input('Nombre del módulo: ').lower()
createFolder(f'apis/modules/{schema}')
createInit(schema)
importModule(schema)