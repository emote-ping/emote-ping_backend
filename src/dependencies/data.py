import matplotlib.pyplot as plt
from typing import List
import numpy as np
from sklearn import datasets
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import StandardScaler



temp_mapping = {
    "temp0": "0C",
    "temp10": "10C",
    "temp20": "20C",
    "temp30": "30C",
    "temp40": "40C"
}

dim1, dim2 = 'arousal', 'valence'
iris = datasets.load_iris()

def parseData(data:List, vIndex:int, aIndex:int) -> List:
    newData = []
    for values in data:
        newData.append((values[vIndex + 2],values[aIndex + 2])) # (valence, arousal)
    return newData

def formatEndOfList(data:list):
    lastVal = data[-1]
    data = data[:-1]
    start = lastVal.find('"')
    end = lastVal.find('"', start+1)
    data.append(lastVal[start+1:end])
    lastVal = lastVal[end+1:].strip().replace(',', '-').split('-')
    for val in lastVal:
        data.append(val)
    return data

def is_float(num):
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
    with open('./src/dependencies/dte_exp1.csv', 'r') as rFile:
        data = rFile.readlines()
        guidlines = data[0].strip().replace(',', '-').split('-')
        val_index, arou_index, emot_index = guidlines.index('valence'), guidlines.index('arousal'), guidlines.index('emotion')
        data = data[1:]
        data = reformatList(data=data,emotion_index=emot_index)
    value = parseData(data, val_index, arou_index)
    return data, guidlines


def convert_dict():
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
    return dict_values


def myplot(x_axis, y_axis, coeff, labels=None):
    xs = x_axis
    ys = y_axis
    n = coeff.shape[0]

    scalex = 1.0 / (xs.max() - xs.min())
    scaley = 1.0 / (ys.max() - ys.min())
    plt.scatter(xs * scalex, ys * scaley, c=y)
    for i in range(n):
        plt.arrow(0, 0, coeff[i, 1], color='r', alpha=0.5)
        if not labels:
            plt.text(coeff[i, 0] * 1.15, coeff[i, 1] * 1.15, f"var{i+1}", color='g', ha='center', va='center')
        else:
            plt.text(coeff[i, 0] * 1.15, coeff[i, 1] * 1.15, label[i], color='g', ha='center', va='center')
        plt.xlim(-4, 4)
        plt.ylim(-4, 4)
        plt.xlabel('Valence')
        plt.ylabel('Arousal')
        plt.grid()

def create_graph():
    dict_values = convert_dict()
    valence = list()
    temp = list()
    arousal = list()
    for val in dict_values:
        valence.append(val.get(dim2))
        arousal.append(val.get(dim1))
        temp.append(val.get('temp_cat'))
    
    scaler = StandardScaler()
    data = [valence, arousal]
    scaler.fit(data)
    valence = scaler.transform(data)
    pca = PCA(n_components=2)
    x_new = pca.fit_transform(temp)

    myplot(x_new, np.transpose(pca.components_[0:1, :]))
    plt.show

create_graph()