from typing import List


temp_mapping = {
    "temp0": "0C",
    "temp10": "10C",
    "temp20": "20C",
    "temp30": "30C",
    "temp40": "40C"
}

dim1, dim2 = 'arousal', 'valence'

def parseData(data:List, vIndex:int, aIndex:int) -> List:
    newData = []
    for values in data:
        newData.append((values[vIndex + 2],values[aIndex + 2])) # (valence, arousal)
    return newData

def formatEndOfList(data:list) -> List:
    lastVal = data[-1]
    data = data[:-1]
    start = lastVal.find('"')
    end = lastVal.find('"', start+1)
    data.append(lastVal[start+1:end])
    lastVal = lastVal[end+1:].strip().replace(',', '-').split('-')
    for val in lastVal:
        data.append(val)
    return data

def is_float(num) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False

def reformatList(data:List, emotion_index) -> List:
    formatedList = []
    for val in data:
        val = val.strip().replace(',', '-', emotion_index).split('-')
        val = formatEndOfList(data=val)
        for index in range(len(val)):    
            if is_float(val[index]):
                val[index] = float(val[index])

        val = [x for x in val if x != '']
        formatedList.append(val)

    return formatedList

def read_csv():
    data = []
    with open('src/dependencies/dte_exp1.csv', 'r') as rFile:
        data = rFile.readlines()
        guidlines = data[0].strip().replace(',', '-').split('-')
        val_index, arou_index, emot_index = guidlines.index('valence'), guidlines.index('arousal'), guidlines.index('emotion')
        data = data[1:]
        data = reformatList(data=data,emotion_index=emot_index)
    value = parseData(data, val_index, arou_index)
    return data, guidlines

    
def dropSets(data:List) -> List:
    simplified_data = []
    for value in data:
        if value.get('response') == 5:
            simplified_data.append(value)
    data = simplified_data
    return data

def convert_dict() -> List:
    # This is so we can set this with **kwargs
    values, keys = read_csv()
    dict_values = []
    for value in values:
        emptyDict = dict()
        for index in range(len(value)):
            if keys[index][:4] == 'temp':
                emptyDict[keys[index]] = temp_mapping[value[index]]
            else:
                emptyDict[keys[index]] = value[index]
        dict_values.append(emptyDict)
    dict_values = dropSets(dict_values)
    return dict_values

