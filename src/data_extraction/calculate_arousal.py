
class user_data:
    def __init__(self, language, resting_hr):
        self.language = language
        self.resting_hr = resting_hr
        self.current_hr = resting_hr
        self.bias = self.__calculateBias()
    
    def __calculateBias(self):
        bias_data = {
            "English": 6.12,
            "Spanish": 6.14,
            "Japanese": 5.29,
            "Chinese": 5.99
        }
        return bias_data[self.language]
    
    def estimate_valence(self):
        arousal = self.predict_arousal()
        radical = (1**2) - (arousal**2)
        return (abs(radical)) ** (1 / 2)

    def collect_current_hr(self, current_hr):
        self.current_hr = current_hr

    def predict_arousal(self):
        deltaHR = self.current_hr - self.resting_hr
        f_inv_y = (((5 / 2) * deltaHR) ** 1.56) - 1
        return f_inv_y / self.bias
    


class Temperature:
    def __init__(self, val, temp_type:str = 'C'):
        self.temp = val
        self.temp_type = temp_type.upper()

        if temp_type == 'F':
            self.temp = self.__convert_FtoC()
        elif temp_type == 'K':
            self.temp = self.__convert_KtoC()
    

    def __convert_FtoC(self):
        return (self.temp - 32) * (5/9)
    
    def __convert_KtoC(self):
        return self.temp - 273.15
    
    def roundTo10(self):
        if self.temp < 5:
            return 0
        elif 5 <= self.temp < 15:
            return 10
        elif 15 <= self.temp < 25:
            return 20
        elif 25 <= self.temp < 35:
            return 30
        else:
            return 40
    

# format: [0C, 10C, 20C, 30C, 40C]
# scale 0.0-4.0 with 4.0 being the most accurate
defaults_emotions_based_on_outside_temp = {
    'tense/bothered': [2.09, 2.13, 2.21, 2.83, 3.33],
    'jittery/bothered': [1.99, 2.13, 2.24, 2.88, 3.18],
    'active/alert': [1.35, 2.02, 3.19, 3.31, 3.06],
    'energetic/excited': [1.28, 1.85, 2.95, 3.49, 3.44],
    'enthusiastic/inspired': [1.3, 1.9, 3.01, 3.33, 3.18],
    'happy/satisfied': [1.36, 2.15, 3.55, 3.24, 2.46],
    'secure/at ease': [1.71, 2.46,3.69, 2.76, 1.8],
    'relaxed/calm': [2.11, 2.8, 3.64, 2.51, 1.53],
    'passive/quiet': [3.02, 3.14, 2.9, 1.97, 1.61],
    'dull/bored': [3.09, 3.0, 2.41, 1.98, 1.8],
    'blue/uninspired': [3.66, 3.17, 2.25, 1.72, 1.61],
    'unhappy/dissatisfied':[3.11, 2.64, 2.11, 2.16, 2.53]
}


