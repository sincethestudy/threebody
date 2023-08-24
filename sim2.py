import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go

m1 = m2 = m3 = 1  # Masses
G = 1  # Gravitational constant

# Initial positions and velocities
state0 = np.array([1, 0, 0,  # x, y, z for body 1
                   0, 1, 0,  # x, y, z for body 2
                  -1, -1, 0, # x, y, z for body 3
                   0.1, 0.2, 0,  # vx, vy, vz for body 1
                   -0.2, 0.1, 0,  # vx, vy, vz for body 2
                   0.1, -0.1, 0])  # vx, vy, vz for body 3

def deriv(state, t):
    r12 = np.sqrt((state[0]-state[3])**2 + (state[1]-state[4])**2 + (state[2]-state[5])**2)
    r13 = np.sqrt((state[0]-state[6])**2 + (state[1]-state[7])**2 + (state[2]-state[8])**2)
    r23 = np.sqrt((state[3]-state[6])**2 + (state[4]-state[7])**2 + (state[5]-state[8])**2)
    
    dv1dt = -G*m2*(state[0:3]-state[3:6])/r12**3 - G*m3*(state[0:3]-state[6:9])/r13**3
    dv2dt = -G*m1*(state[3:6]-state[0:3])/r12**3 - G*m3*(state[3:6]-state[6:9])/r23**3
    dv3dt = -G*m1*(state[6:9]-state[0:3])/r13**3 - G*m2*(state[6:9]-state[3:6])/r23**3

    return np.concatenate((state[9:12], state[12:15], state[15:18], dv1dt, dv2dt, dv3dt))

t = np.linspace(0, 10, 5000)  # Simulate for 10 time units
state = odeint(deriv, state0, t)

# Create subplot
fig = go.Figure()

# Add empty traces for paths
trace1 = go.Scatter3d(x=[], y=[], z=[], mode='lines', name='Body 1 Path')
trace2 = go.Scatter3d(x=[], y=[], z=[], mode='lines', name='Body 2 Path')
trace3 = go.Scatter3d(x=[], y=[], z=[], mode='lines', name='Body 3 Path')
fig.add_trace(trace1)
fig.add_trace(trace2)
fig.add_trace(trace3)

# Add empty traces for markers
marker1 = go.Scatter3d(x=[], y=[], z=[], mode='markers', name='Body 1')
marker2 = go.Scatter3d(x=[], y=[], z=[], mode='markers', name='Body 2')
marker3 = go.Scatter3d(x=[], y=[], z=[], mode='markers', name='Body 3')
fig.add_trace(marker1)
fig.add_trace(marker2)
fig.add_trace(marker3)

frames = [go.Frame(data=[go.Scatter3d(x=state[:k+1,0], y=state[:k+1,1], z=state[:k+1,2], mode='lines'),
                         go.Scatter3d(x=state[:k+1,3], y=state[:k+1,4], z=state[:k+1,5], mode='lines'),
                         go.Scatter3d(x=state[:k+1,6], y=state[:k+1,7], z=state[:k+1,8], mode='lines'),
                         go.Scatter3d(x=[state[k,0]], y=[state[k,1]], z=[state[k,2]], mode='markers'),
                         go.Scatter3d(x=[state[k,3]], y=[state[k,4]], z=[state[k,5]], mode='markers'),
                         go.Scatter3d(x=[state[k,6]], y=[state[k,7]], z=[state[k,8]], mode='markers')]) for k in range(1, len(t), 100)]

# Add frames to figure
fig.frames = frames

# Update layout
fig.update_layout(updatemenus=[dict(type="buttons",
                                    buttons=[dict(label="Play",
                                                  method="animate",
                                                  args=[None, {"frame": {"duration": 30, "redraw": True},
                                                               "fromcurrent": True, "transition": {"duration": 300}}])])])

fig.update_layout(scene=dict(xaxis=dict(range=[-2, 2]), yaxis=dict(range=[-2, 2]), zaxis=dict(range=[-2, 2]),
                             aspectmode='cube'))

fig.show()
