# read json and add zero for non existing values
from datetime import datetime, timedelta
import json

file_path = 'dataset/qload.json'

with open(file_path) as f:
    data = json.load(f)

for i in ['1', '2', '3', '4', '5']:
    if i not in data:
        data[i] = {}
        data[i]['profile'] = {}
        #add "00:00" to "23:55" with zero value with 5 minutes interval make sure 00:00, 00:05 instead of 0:05 avoid 00:00:00
        for j in range(0, 24*60, 5):
            time = str(timedelta(minutes=j))
            if len(time) == 7:
                time = '0' + time
                time = time[:-3]
            data[i]['profile'][time] = 0.001
        
        # "Pnom_a": 123,
        # "Pnom_b": 123,
        # "Pnom_c": 123,
        # "comment": "p load profile for 5 minutes"
        data[i]['Pnom_a'] = 1
        data[i]['Pnom_b'] = 1
        data[i]['Pnom_c'] = 1
        data[i]['comment'] = 'p load profile for 5 minutes'


# save the data
with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)

a = 1