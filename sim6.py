import plotly.graph_objects as go
import json
import numpy as np

def process_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    print(len(data['position']))
    
    data_cut = {}
    data_cut['position'] = [data['position'][i:i+9] for i in range(0, len(data['position']), 5*9)]
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

def create_frames(x1, y1, x2, y2, x3, y3, N=175, OG=False):
    frames = []

    if OG:
        for i in range(1, len(x1)):
            frames.append(go.Frame(data=[
                go.Scatter(x=x1[max(0,i-N+1):i+1], y=y1[max(0,i-N+1):i+1], mode="lines", name="Entity 1", line=dict(width=3)),
                go.Scatter(x=x1[i:i+1], y=y1[i:i+1], mode="markers", name="Entity 1 Marker", marker=dict(size=20)),
                go.Scatter(x=x2[max(0,i-N+1):i+1], y=y2[max(0,i-N+1):i+1], mode="lines", name="Entity 2", line=dict(width=3)),
                go.Scatter(x=x2[i:i+1], y=y2[i:i+1], mode="markers", name="Entity 2 Marker", marker=dict(size=20)),
                go.Scatter(x=x3[max(0,i-N+1):i+1], y=y3[max(0,i-N+1):i+1], mode="lines", name="Entity 3", line=dict(width=3)),
                go.Scatter(x=x3[i:i+1], y=y3[i:i+1], mode="markers", name="Entity 3 Marker", marker=dict(size=20))
            ]))
    else:
        sizes = np.linspace(5, 20, len(x1))
        widths = np.linspace(1, 3, len(x1))
        for i in range(1, len(x1)):
            frames.append(go.Frame(data=[
                go.Scatter(x=x1[max(0,i-N+1):i+1], y=y1[max(0,i-N+1):i+1], mode="lines", name="Entity 1", line=dict(width=widths[i])),
                go.Scatter(x=x1[i:i+1], y=y1[i:i+1], mode="markers", name="Entity 1 Marker", marker=dict(size=sizes[i])),
                go.Scatter(x=x2[max(0,i-N+1):i+1], y=y2[max(0,i-N+1):i+1], mode="lines", name="Entity 2", line=dict(width=widths[i])),
                go.Scatter(x=x2[i:i+1], y=y2[i:i+1], mode="markers", name="Entity 2 Marker", marker=dict(size=sizes[i])),
                go.Scatter(x=x3[max(0,i-N+1):i+1], y=y3[max(0,i-N+1):i+1], mode="lines", name="Entity 3", line=dict(width=widths[i])),
                go.Scatter(x=x3[i:i+1], y=y3[i:i+1], mode="markers", name="Entity 3 Marker", marker=dict(size=sizes[i]))
            ]))
    return frames



x1, y1, x2, y2, x3, y3 = process_json_data('base_traj_2.json')
frames1 = create_frames(x1, y1, x2, y2, x3, y3)

x1_2, y1_2, x2_2, y2_2, x3_2, y3_2 = process_json_data('new_child_traj.json')
frames2 = create_frames(x1_2, y1_2, x2_2, y2_2, x3_2, y3_2)


print(len(x1), len(x1_2))



frames1_e = create_frames(np.concatenate((x1,x1,x1)), np.concatenate((y1,y1,y1)), np.concatenate((x2,x2,x2)), np.concatenate((y2,y2,y2)), np.concatenate((x3,x3,x3)), np.concatenate((y3, y3,y3)), OG=True)

x1_2_e, y1_2_e, x2_2_e, y2_2_e, x3_2_e, y3_2_e = process_json_data('new_child_traj_extended_time.json')

x1_2_e2, y1_2_e2, x2_2_e2, y2_2_e2, x3_2_e2, y3_2_e2 = process_json_data('new_child_traj_extended_time_2.json')

print(len(x1_2_e), len(x1_2_e2))

frames2_e = create_frames(np.concatenate((x1_2,x1_2_e,x1_2_e2)), np.concatenate((y1_2,y1_2_e,y1_2_e2)), np.concatenate((x2_2,x2_2_e,x2_2_e2)), np.concatenate((y2_2,y2_2_e,y2_2_e2)), np.concatenate((x3_2,x3_2_e,x3_2_e2)), np.concatenate((y3_2, y3_2_e, y3_2_e2)))


frames = [go.Frame(data=f1['data'] + f2['data']) for f1, f2 in zip(frames1_e, frames2_e)]


data=[
    go.Scatter(x=x1[:1], y=y1[:1], mode="lines", name="Entity 1", line=dict(color='darkblue')),
    go.Scatter(x=x1[:1], y=y1[:1], mode="markers", name="Entity 1 Marker", marker=dict(size=20, color='darkblue')),
    go.Scatter(x=x2[:1], y=y2[:1], mode="lines", name="Entity 2", line=dict(color='green')),
    go.Scatter(x=x2[:1], y=y2[:1], mode="markers", name="Entity 2 Marker", marker=dict(size=20, color='green')),
    go.Scatter(x=x3[:1], y=y3[:1], mode="lines", name="Entity 3", line=dict(color='red')),
    go.Scatter(x=x3[:1], y=y3[:1], mode="markers", name="Entity 3 Marker", marker=dict(size=20, color='red')),
]


# Add the data from the second JSON
data.extend([
    go.Scatter(x=x1_2[:1], y=y1_2[:1], mode="lines", name="Entity 1_2", line=dict(color='violet')),
    go.Scatter(x=x1_2[:1], y=y1_2[:1], mode="markers", name="Entity 1_2 Marker", marker=dict(size=5, color='violet')),
    go.Scatter(x=x2_2[:1], y=y2_2[:1], mode="lines", name="Entity 2_2", line=dict(color='cyan')),
    go.Scatter(x=x2_2[:1], y=y2_2[:1], mode="markers", name="Entity 2_2 Marker", marker=dict(size=5, color='cyan')),
    go.Scatter(x=x3_2[:1], y=y3_2[:1], mode="lines", name="Entity 3_2", line=dict(color='yellow')),
    go.Scatter(x=x3_2[:1], y=y3_2[:1], mode="markers", name="Entity 3_2 Marker", marker=dict(size=5, color='yellow')),
])


fig = go.Figure(
    data=data,
    layout=go.Layout(
        template='plotly_dark',
        updatemenus=[dict(type="buttons",
                        showactive=False,
                        buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None, 
                                            {"frame": {"duration": 10, "redraw": True},
                                            "fromcurrent": True, 
                                            "transition": {"duration": 10, "easing": "quadratic-in-out"}, 
                                            "mode": "immediate"}])])],
        xaxis=dict(range=[-2, 2]),  
        yaxis=dict(range=[-2, 10]),  
    ),
    frames=frames
)

fig.show()
