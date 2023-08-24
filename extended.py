import json
import numpy as np

import random

import plotly.graph_objects as go
import json
import numpy as np

from scipy.interpolate import interp1d

def resample_data(data, new_length):
    old_length = len(data['position']) // 9
    old_indices = np.linspace(0, old_length - 1, old_length)
    new_indices = np.linspace(0, old_length - 1, new_length)

    # Reshape the array to allow separate handling of each position component
    reshaped_data = np.array(data['position']).reshape(old_length, 9)

    # Create an empty array for the resampled data
    resampled_data = np.empty((new_length, 9))

    for i in range(9):
        component = reshaped_data[:, i]
        interpolator = interp1d(old_indices, component)
        resampled_data[:, i] = interpolator(new_indices)

    # Flatten the resampled_data and convert it back to list format
    return {'position': resampled_data.flatten().tolist()}


# Load your trajectory data
with open('base_traj_2.json', 'r') as f:
    base_data = json.load(f)

base_length = len(base_data['position']) // 9


double_extend = {}

with open('child_traj_1.json', 'r') as f:
    data = json.load(f)

    data = resample_data(data, base_length)


    ting = len(data['position'])//9

    for i in range(0, len(data['position']), 9):
        data['position'][1 + i] += ting*0.0005 + i/9*0.001
        data['position'][4 + i] += ting*0.0005 + i/9*0.001
        data['position'][7 + i] += ting*0.0005 + i/9*0.001

        data['position'][0 + i] /= 2
        data['position'][3 + i] /= 2
        data['position'][6 + i] /= 2

        

    print(data['position'][100:110])

    with open('new_child_traj_extended_time.json', 'w') as f:
        json.dump(data, f)

    for i in range(0, len(data['position']), 9):
        data['position'][1 + i] +=  ting*0.001 + i/9*0.002
        data['position'][4 + i] +=  ting*0.001 + i/9*0.002
        data['position'][7 + i] +=  ting*0.001 + i/9*0.002

    print(data['position'][100:110])

    with open('new_child_traj_extended_time_2.json', 'w') as f:
        json.dump(data, f)





