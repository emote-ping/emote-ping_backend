import xml.etree.ElementTree as ET
import pandas as pd


def calculateArousal(pulse, language):
    bias = {
        "English": 6.12,
        "Spanish": 6.14,
        "Japanese": 5.29,
        "Chinese": 5.99
    }
    return ((((5/2) * pulse) ** 1.56) - 1) / bias[language]

def extract_heart_rate():
    tree = ET.parse('apple_health_export/export.xml')
    root = tree.getroot()
    record_list = [x.attrib for x in root.iter('Record')]

    data = pd.DataFrame(record_list)
    for col in ['creationDate', 'startDate', 'endDate']:
        data[col] = pd.to_datetime(data[col])
    
    data['value'] = pd.to_numeric(data['value'], errors='coerce')
    