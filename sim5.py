import plotly.graph_objects as go
import json
import numpy as np

def process_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    print(len(data['position']))
    
    data_cut = {}
    data_cut['position'] = [data['position'][i:i+9] for i in range(0, len(data['position']), 10*9)]
    data_cut['position'] = [item for sublist in data_cut['position'] for item in sublist]
    # data_cut['position'] = data['position']
    
    x1 = data_cut['position'][::9]
    y1 = data_cut['position'][1::9]
    t1 = data_cut['position'][2::9]

    x2 = data_cut['position'][3::9]
    y2 = data_cut['position'][4::9]
    t2 = data_cut['position'][5::9]

    x3 = data_cut['position'][6::9]
    y3 = data_cut['position'][7::9]
    t3 = data_cut['position'][8::9]

    t1 = np.array(t1)
    t2 = np.array(t2)
    t3 = np.array(t3)

    t_new = np.linspace(min(t1.min(), t2.min(), t3.min()), max(t1.max(), t2.max(), t3.max()), len(t1)*1)

    x1_new = np.interp(t_new, t1, x1)
    y1_new = np.interp(t_new, t1, y1)
    x2_new = np.interp(t_new, t2, x2)
    y2_new = np.interp(t_new, t2, y2)
    x3_new = np.interp(t_new, t3, x3)
    y3_new = np.interp(t_new, t3, y3)

    #just set the new time to be the same as the old time
    # x1_new = x1
    # y1_new = y1
    # x2_new = x2
    # y2_new = y2
    # x3_new = x3
    # y3_new = y3


    return x1_new, y1_new, x2_new, y2_new, x3_new, y3_new

def create_frames(x1, y1, x2, y2, x3, y3, N=175):
    frames = []
    for i in range(1, len(x1)):
        frames.append(go.Frame(data=[
            go.Scatter3d(x=x1[max(0,i-N+1):i+1], y=y1[max(0,i-N+1):i+1], z=[0]*(min(i+1,N)), mode="lines", name="Entity 1"),
            go.Scatter3d(x=x1[i:i+1], y=y1[i:i+1], z=[0]*1, mode="markers", name="Entity 1 Marker"),
            go.Scatter3d(x=x2[max(0,i-N+1):i+1], y=y2[max(0,i-N+1):i+1], z=[0]*(min(i+1,N)), mode="lines", name="Entity 2"),
            go.Scatter3d(x=x2[i:i+1], y=y2[i:i+1], z=[0]*1, mode="markers", name="Entity 2 Marker"),
            go.Scatter3d(x=x3[max(0,i-N+1):i+1], y=y3[max(0,i-N+1):i+1], z=[0]*(min(i+1,N)), mode="lines", name="Entity 3"),
            go.Scatter3d(x=x3[i:i+1], y=y3[i:i+1], z=[0]*1, mode="markers", name="Entity 3 Marker")
        ]))
    return frames

x1, y1, x2, y2, x3, y3 = process_json_data('base_traj_2.json')
frames1 = create_frames(x1, y1, x2, y2, x3, y3)

x1_2, y1_2, x2_2, y2_2, x3_2, y3_2 = process_json_data('new_child_traj.json')
frames2 = create_frames(x1_2, y1_2, x2_2, y2_2, x3_2, y3_2)




frames1_e = create_frames(np.concatenate((x1,x1,x1)), np.concatenate((y1,y1,y1)), np.concatenate((x2,x2,x2)), np.concatenate((y2,y2,y2)), np.concatenate((x3,x3,x3)), np.concatenate((y3, y3,y3)))

x1_2_e, y1_2_e, x2_2_e, y2_2_e, x3_2_e, y3_2_e = process_json_data('new_child_traj_extended_time.json')

x1_2_e2, y1_2_e2, x2_2_e2, y2_2_e2, x3_2_e2, y3_2_e2 = process_json_data('new_child_traj_extended_time_2.json')

frames2_e = create_frames(np.concatenate((x1_2,x1_2_e,x1_2_e2)), np.concatenate((y1_2,y1_2_e,y1_2_e2)), np.concatenate((x2_2,x2_2_e,x2_2_e2)), np.concatenate((y2_2,y2_2_e,y2_2_e2)), np.concatenate((x3_2,x3_2_e,x3_2_e2)), np.concatenate((y3_2, y3_2_e, y3_2_e2)))


# Combine the frames
frames = [go.Frame(data=f1['data'] + f2['data']) for f1, f2 in zip(frames1_e, frames2_e)]


# x1_2, y1_2, x2_2, y2_2, x3_2, y3_2 = process_json_data('new_child_traj_upsampled.json')
# frames_temp = create_frames(x1_2, y1_2, x2_2, y2_2, x3_2, y3_2)
# frames = frames_temp



# Create the initial data
data=[
    go.Scatter3d(x=x1[:1], y=y1[:1], z=[0]*1, mode="lines", name="Entity 1"),
    go.Scatter3d(x=x1[:1], y=y1[:1], z=[0]*1, mode="markers", name="Entity 1 Marker"),
    go.Scatter3d(x=x2[:1], y=y2[:1], z=[0]*1, mode="lines", name="Entity 2"),
    go.Scatter3d(x=x2[:1], y=y2[:1], z=[0]*1, mode="markers", name="Entity 2 Marker"),
    go.Scatter3d(x=x3[:1], y=y3[:1], z=[0]*1, mode="lines", name="Entity 3"),
    go.Scatter3d(x=x3[:1], y=y3[:1], z=[0]*1, mode="markers", name="Entity 3 Marker"),
]

# Add the data from the second JSON
data.extend([
    go.Scatter3d(x=x1_2[:1], y=y1_2[:1], z=[0]*1, mode="lines", name="Entity 1_2"),
    go.Scatter3d(x=x1_2[:1], y=y1_2[:1], z=[0]*1, mode="markers", name="Entity 1_2 Marker"),
    go.Scatter3d(x=x2_2[:1], y=y2_2[:1], z=[0]*1, mode="lines", name="Entity 2_2"),
    go.Scatter3d(x=x2_2[:1], y=y2_2[:1], z=[0]*1, mode="markers", name="Entity 2_2 Marker"),
    go.Scatter3d(x=x3_2[:1], y=y3_2[:1], z=[0]*1, mode="lines", name="Entity 3_2"),
    go.Scatter3d(x=x3_2[:1], y=y3_2[:1], z=[0]*1, mode="markers", name="Entity 3_2 Marker"),
])

fig = go.Figure(
    data=data,
    layout=go.Layout(
        updatemenus=[dict(type="buttons",
                          showactive=False,
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None, 
                                              {"frame": {"duration": 1, "redraw": True},
                                               "fromcurrent": True, 
                                               "transition": {"duration": 1, "easing": "quadratic-in-out"}, 
                                               "mode": "immediate"}])])],
        scene=dict(
            xaxis=dict(range=[-3, 2]),  
            yaxis=dict(range=[-2, 10]),  
            zaxis=dict(range=[-2, 2]),  
            aspectmode='cube'  
        )
    ),
    frames=frames
)

fig.show()
