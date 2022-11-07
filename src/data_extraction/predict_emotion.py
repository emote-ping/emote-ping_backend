import pandas as pd
from typing import List
from dependencies.data import convert_dict
from data_extraction.calculate_arousal import Temperature


def determine_temp(orig_temp:str) -> Temperature:
    orig_temp = orig_temp.strip('°').strip()
    l_index = len(orig_temp) - 1
    temp_type = orig_temp[-1] if orig_temp[-1].isalpha() else 'C'
    temp = Temperature(val=float(orig_temp[:l_index - 1]), temp_type=temp_type)

    return temp

def constrain_temp_cat(temper:Temperature) -> List:
    s_temp = f"{temper.roundTo10()}C"
    
    baseline_data = convert_dict()
    constrained_data = list()

    for val in baseline_data:
        if s_temp == val.get('temp_cat'):
            constrained_data.append(val)
    
    return constrained_data

def check_association(value, data:List[tuple]) -> bool:
    for val in data:
        if val[1] == value:
            return True
    return

def sum_sample_space(predictions:List) -> List:
    emotions = []

    for val in predictions:
        if not check_association(val['emotion'], emotions):
            emotions.append([1, val['emotion']])
        else:
            for emote in emotions:
                if emote == val['emotion']:
                    emote[1] += 1
    return sorted(emotions, reverse=True)

def predict_top_3(predictions:List) -> tuple:
    vals = sum_sample_space(predictions=predictions)

    return vals[0][1], vals[1][1], vals[2][1]



    



