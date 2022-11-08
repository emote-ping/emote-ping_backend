import xml.etree.ElementTree as ET
import pandas as pd
from heartbridge import Health
from data_extraction.calculate_arousal import user_data
from dependencies.request_temp import get_current_weather, get_lon_and_lat
from data_extraction.predict_emotion import determine_temp, constrain_temp_cat, predict_top_3




# incoming_shortcuts_json = './data_extraction/apple_health_export/export.csv'
# health = Health()
# health.load_from_shortcuts(data=incoming_shortcuts_json)


# def extract_heart_rate():
#     tree = ET.parse('apple_health_export/export.xml')
#     root = tree.getroot()
#     record_list = [x.attrib for x in root.iter('Record')]

#     data = pd.DataFrame(record_list)
#     for col in ['creationDate', 'startDate', 'endDate']:
#         data[col] = pd.to_datetime(data[col])
    
#     data['value'] = pd.to_numeric(data['value'], errors='coerce')
#     print(health.reading_type_slug)
    

def create_user(language='English', hr=97.2):
    return user_data(language=language, resting_hr=hr)


def promptZipcode():
    zipcode = str(input("Please enter a zipcode -> "))
    return zipcode

def cont():
    again = str(input("Would you like to try another -> "))
    return again == 'y'


if __name__ == '__main__':
    user = create_user()
    # extract_heart_rate()
    again = True
    while again:
        z_code = promptZipcode()
        lat, lon = get_lon_and_lat(z_code)
        temper = get_current_weather(lat, lon)
        temper = determine_temp(orig_temp=temper)
        constraints = constrain_temp_cat(temper=temper)
        predictions = predict_top_3(predictions=constraints)

        print(f"""You must be feeling one of the three sets of emotions below:
            1. {predictions[0]}
            2. {predictions[1]}
            3. {predictions[2]}
        """)
        again = cont()
    