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

with open('trajectory_test.json', 'r') as f:
    child_traj_1_data = json.load(f)

base_length = len(base_data['position']) // 9
child_traj_1_data = resample_data(child_traj_1_data, base_length)

with open('new_child_traj_upsampled.json', 'w') as f:
    json.dump(child_traj_1_data, f)


x1 = base_data['position'][::9]
y1 = base_data['position'][1::9]
t1 = base_data['position'][2::9]

x2 = base_data['position'][3::9]
y2 = base_data['position'][4::9]
t2 = base_data['position'][5::9]

x3 = base_data['position'][6::9]
y3 = base_data['position'][7::9]
t3 = base_data['position'][8::9]

t1 = np.array(t1)
t2 = np.array(t2)
t3 = np.array(t3)

G = 6.67430e-8  # gravitational constant
m_base = 1  # mass of bodies in base system
m_child = 1  # mass of bodies in child system

x_child = [-0.7, 0, 1]
y_child = [-2, -2, -2]
z_child = [0, 0, 0]
vx_child = [0, 0, 0]
vy_child = [0.0005, 0.0005, 0.0005]
vz_child = [0, 0, 0]

x_child_all = [list(x_child)]
y_child_all = [list(y_child)]
z_child_all = [list(t3)]
vx_child_all = [list(vx_child)]
vy_child_all = [list(vy_child)]
vz_child_all = [list(t3)]

for frame in range(1, len(x1)):
    for i in range(3):
        for j in range(3):
            x_base = [x1[frame], x2[frame], x3[frame]][j]
            y_base = [y1[frame], y2[frame], y3[frame]][j]

            dx = x_base - x_child[i]
            dy = y_base - y_child[i]
            dz = 0
            r = np.sqrt(dx**2 + dy**2 + dz**2)
            F = G * m_base * m_child / r**3


            vx_child[i] += F * dx
            vy_child[i] += F * dy
            vz_child[i] += 0

    # Update positions
    x_child = [x + vx for x, vx in zip(x_child, vx_child)]
    y_child = [y + vy for y, vy in zip(y_child, vy_child)]
    z_child = [z + vz for z, vz in zip(z_child, vz_child)]

    # Store new positions and velocities
    x_child_all.append(list(x_child))
    y_child_all.append(list(y_child))
    z_child_all.append(list(z_child))
    vx_child_all.append(list(vx_child))
    vy_child_all.append(list(vy_child))
    vz_child_all.append(list(vz_child))


# Assuming the child_traj_1_data structure is similar to base_data
x_child_1 = child_traj_1_data['position'][::9]
y_child_1 = child_traj_1_data['position'][1::9]
time_child_1 = child_traj_1_data['position'][2::9]

x_child_2 = child_traj_1_data['position'][3::9]
y_child_2 = child_traj_1_data['position'][4::9]
time_child_2 = child_traj_1_data['position'][5::9]

x_child_3 = child_traj_1_data['position'][6::9]
y_child_3 = child_traj_1_data['position'][7::9]
time_child_3 = child_traj_1_data['position'][8::9]


# # Assuming the lengths of x1 and x_child_1 are the same
for i in range(0, len(x1)):
    for j in range(3):
        t = (i / len(x1))  # time parameter for interpolation, 0 to 1

        x_child_t = [x_child_1[i], x_child_2[i], x_child_3[i]][j]
        y_child_t = [y_child_1[i], y_child_2[i], y_child_3[i]][j]

        # Interpolate between the child system's trajectory and the base system's trajectory
        x_child_all[i][j] = (x_child_all[i][j]*(1-t) + x_child_t*(t))
        y_child_all[i][j] = (y_child_all[i][j]*(1-t) + y_child_t*(t) + 0.001*i)


# Now we create a single list that represents the complete trajectory 
new_child_traj_list = []
for i in range(len(x_child_all)):
    # Flatten the lists and extend the main list
    new_child_traj_list.append(x_child_all[i][0]/2)
    new_child_traj_list.append(y_child_all[i][0]/2)
    new_child_traj_list.append(t3[i])

    new_child_traj_list.append(x_child_all[i][1]/2)
    new_child_traj_list.append(y_child_all[i][1]/2)
    new_child_traj_list.append(t3[i])

    new_child_traj_list.append(x_child_all[i][2]/2)
    new_child_traj_list.append(y_child_all[i][2]/2)
    new_child_traj_list.append(t3[i])

print(len(new_child_traj_list))

new_child_traj = {'position': new_child_traj_list}

with open('new_child_traj.json', 'w') as f:
    json.dump(new_child_traj, f)
