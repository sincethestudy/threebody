import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go
from scipy.integrate import solve_ivp



class Body:
    def __init__(self, mass, initial_position, initial_velocity):
        self.mass = mass
        self.position = np.array(initial_position)
        self.velocity = np.array(initial_velocity)


class ThreeBodySystem:
    G = 1  # Gravitational constant

    def __init__(self, body1, body2, body3):
        self.bodies = [body1, body2, body3]

    def deriv(self, _, state):
        r12 = np.sqrt((state[0] - state[3]) ** 2 + (state[1] - state[4]) ** 2 + (state[2] - state[5]) ** 2)
        r13 = np.sqrt((state[0] - state[6]) ** 2 + (state[1] - state[7]) ** 2 + (state[2] - state[8]) ** 2)
        r23 = np.sqrt((state[3] - state[6]) ** 2 + (state[4] - state[7]) ** 2 + (state[5] - state[8]) ** 2)

        dv1dt = -self.G * self.bodies[1].mass * (state[0:3] - state[3:6]) / r12 ** 3 - \
                self.G * self.bodies[2].mass * (state[0:3] - state[6:9]) / r13 ** 3
        dv2dt = -self.G * self.bodies[0].mass * (state[3:6] - state[0:3]) / r12 ** 3 - \
                self.G * self.bodies[2].mass * (state[3:6] - state[6:9]) / r23 ** 3
        dv3dt = -self.G * self.bodies[0].mass * (state[6:9] - state[0:3]) / r13 ** 3 - \
                self.G * self.bodies[1].mass * (state[6:9] - state[3:6]) / r23 ** 3

        return np.concatenate((state[9:12], state[12:15], state[15:18], dv1dt, dv2dt, dv3dt))

    def solve(self, T, N):
        state0 = np.concatenate((body1.position, body1.velocity, 
                         body2.position, body2.velocity, 
                         body3.position, body3.velocity))
        t = np.linspace(0, T, N)
        
        sol = solve_ivp(self.deriv, (0, T), state0, t_eval=t, method='DOP853')
        
        return sol.t, sol.y.T


# Initial positions and velocities
y0 = [0.716248295713, 0.384288553041, 0.0, 1.245268230896, 2.444311951777, 0.0, 
      0.086172594591, 1.342795868577, 0.0, -0.67522432369, -0.96287961363, 0.0, 
      0.538777980808, 0.481049882656, 0.0, -0.570043907206, -1.481432338147, 0.0]

# Create bodies
body1 = Body(1, y0[0:3], y0[3:6])
body2 = Body(1, y0[6:9], y0[9:12])
body3 = Body(1, y0[12:15], y0[15:18])


# Create system
system = ThreeBodySystem(body1, body2, body3)

# Solve for a duration of one period
T = 8.094721472532424
N = 5000  # Adjust as needed for accuracy vs. computational speed
t, state = system.solve(T, N)



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

fig.update_layout(scene=dict(xaxis=dict(range=[-20, 20]), yaxis=dict(range=[-20, 20]), zaxis=dict(range=[-2, 2]),
                             aspectmode='cube'))

fig.show()
