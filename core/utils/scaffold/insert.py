from pprint import pprint
import re
from colorama import Fore

def getLineValues(input: str):
    valueSearch = re.search('VALUES', input)
    if valueSearch:
        tmpStr = input[valueSearch.end():].strip()
        if re.search(';', tmpStr):
            tmpStr = tmpStr[:-1]
        tmpValues = tmpStr[1:-1]
        values = [val.strip() for val in tmpValues.split(',')]
        return values

def getInputLines():
    output = []
    inputFile = open('core/utils/scaffold/insert_files/data_input.sql')
    lines = inputFile.readlines()
    inputFile.close()
    for line in lines:
        line = line.strip()
        if line != '':
            output.append(line)
    return output

def writeFileOutput(tabla: str, colNames: list, values: list):
    inputFile = open('core/utils/scaffold/insert_files/data_output.py', 'w')
    inputFile.write(f'op.bulk_insert({tabla}, [\n')
    for val in values:
        l = '        {'
        index = 0
        for col in colNames:
            l += f"'{col}':{formatValue(val[index])}"
            index += 1
            if index < len(colNames):
                l += ', '
        l += '},\n'
        inputFile.write(l)
    inputFile.write('\n    ])')
    inputFile.close()

def formatValue(val: str):
    if val in ['true', 'TRUE', 'True']:
        return 'True'
    elif val in ['false', 'FALSE', 'False']:
        return 'False'
    else:
        return val

tabla = input('Tabla: ')
camposCrud = input('Columnas CRUD?: [y/n] ')
colNames = []
colIndex = 1
if camposCrud == 'y':
    colNames.append('create_date')
    colNames.append('user_at')
    colNames.append('activo')
    colIndex = 4
actualLine = '-'
while actualLine != '':
    actualLine = input(f'Nombre de columna {colIndex}: ')
    colIndex += 1
    if actualLine != '':
        colNames.append(actualLine)

values = []
fileLines = getInputLines()
for fLine in fileLines:
    if re.search('VALUES', fLine):
        values.append(getLineValues(fLine))

if len(values) == 0:
    exit()

if len(values[0]) != len(colNames):
    print(Fore.RED, '* El numero de columnas no coincide con el numero de valores', Fore.RESET)
    exit()

writeFileOutput(tabla, colNames, values)
print(Fore.CYAN, '* Scaffold realizado con exito', Fore.RESET)