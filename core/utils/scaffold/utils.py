import re, os

def isNotNullCol(input: str):
    if re.search('nullable=False', input): return True
    else: return False

def getPrimarykey(data):
    output: str = None
    for key in data:
        if data[key]['primaryKey'] == True:
            output = key
    return output

def firstLower(input: str):
    return input[0].lower() + input[1:]

def toSingularWord(input: str):
    if re.search('ies$', input): return input[0:-1]
    elif re.search('(les|tes)$', input): return input[0:-1]
    elif re.search('es$', input): return input[0:-2]
    elif re.search('s$', input): return input[0:-1]
    else: return input

def camelCaseSplit(str, singular=0, firstLower=0):
    tmp = [[str[0]]]
    for c in str[1:]:
        if tmp[-1][-1].islower() and c.isupper():
            tmp.append(list(c))
        else:
            tmp[-1].append(c)

    return [''.join(word) for word in tmp]

def spinalToCamel(word: str, firstUpper: bool=False):
    temp = word.split('_')
    res = temp[0] + ''.join(ele.title() for ele in temp[1:])
    return res[0].upper() + res[1:] if firstUpper else res

def getColumnDataType(line: str):
    if re.search('db.SmallInteger', line) or re.search('db.Integer', line) or re.search('db.BigInteger', line):
        return 'fields.Integer', 'int'
    if re.search('db.Numeric\(.*\)', line) or re.search('db.Float\(.*\)', line):
        return 'fields.Float', 'float'
    if re.search('db.DateTime', line) or re.search('TIMESTAMP', line ):
        return 'fields.DateTime', 'inputs.date_from_iso8601'
    if re.search('db.Boolean', line):
        return 'fields.Boolean', 'inputs.boolean'
    if re.search('db.String', line):
        return 'fields.String', 'str'
    else:
        return None, None

def getSwaggerName(table: str):
    camel = spinalToCamel(table, True)
    swaggerName = ' '.join([word for word in camelCaseSplit(camel)])
    return swaggerName

def createFolder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)