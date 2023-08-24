import numpy as np
from scipy.integrate import solve_ivp
import math
from tqdm import tqdm  # Add this import at the top of your script


initialConditions = {
    "name": "Ovals-with-flourishes",
    "y0": [0.716248295713, 0.384288553041, 1.245268230896, 2.444311951777, 0.086172594591, 1.342795868577, -0.67522432369, -0.96287961363, 0.538777980808, 0.481049882656, -0.570043907206, -1.481432338147],
    "tolerance": 1e-9,
    "period": 8.094721472532424,
    "m": [1, 1, 1],
    "colors": [[255, 255, 255], [255, 255, 255], [255, 255, 255]],  # Assuming RGB colors
    "pointSize": [1, 1, 1]
}


def planar_three_body_derivative(yp, y, t, initial_conditions):
    m0 = initial_conditions['m'][0]
    m1 = initial_conditions['m'][1]
    m2 = initial_conditions['m'][2]
    
    # The first derivative of position is stored in the state vector,
    # so its computation is nothing more than copying part of the
    # state into the result.
    yp[0] = y[2]
    yp[1] = y[3]
    yp[4] = y[6]
    yp[5] = y[7]
    yp[8] = y[10]
    yp[9] = y[11]
    
    # The rest of the function computes the first derivative of
    # velocity, i.e. the acceleration.
    # Attraction between 0-1
    dx = y[4] - y[0]
    dy = y[5] - y[1]
    r3 = (dx * dx + dy * dy) ** 1.5
    dx /= r3
    dy /= r3
    yp[2] = dx * m1
    yp[3] = dy * m1
    yp[6] = -dx * m0
    yp[7] = -dy * m0
    
    # Attraction between 0-2
    dx = y[8] - y[0]
    dy = y[9] - y[1]
    r3 = (dx * dx + dy * dy) ** 1.5
    dx /= r3
    dy /= r3
    yp[2] += dx * m2
    yp[3] += dy * m2
    yp[10] = -dx * m0
    yp[11] = -dy * m0
    
    # Attraction between 1-2
    dx = y[8] - y[4]
    dy = y[9] - y[5]
    r3 = (dx * dx + dy * dy) ** 1.5
    dx /= r3
    dy /= r3
    yp[6] += dx * m2
    yp[7] += dy * m2
    yp[10] -= dx * m1
    yp[11] -= dy * m1

def compute_trajectory(initial_conditions, tolerance=1e-9, period=None):
    y0 = np.array(initial_conditions['y0'])
    t_span = (0, period if period else np.inf)

    state = {'t': 0, 'y': y0}
    result = {'position': [], 't': []}

    def store_step(t, y):
        result['t'].append(t)
        for idx in range(0, len(y), 4):
            result['position'].append([y[idx], y[idx+1], t, y[idx+2], y[idx+3], t])
    
    store_step(state['t'], state['y'])

    yp = np.zeros(y0.shape)
    
    def derivative(t, y):
        planar_three_body_derivative(yp, y, t, initial_conditions)
        return yp

    step = 0
    pbar = tqdm(total=1e6)  # Initialize progress bar
    while step < 1e6:
        step += 1

        if step % 1000 == 0:  # Update progress bar every 1000 steps
            pbar.update(1000)

        sol = solve_ivp(
            fun=derivative,
            t_span=t_span,
            y0=state['y'],
            method='DOP853',
            atol=tolerance,
            rtol=tolerance,
        )

        print(f"solution status: {sol.status}, message: {sol.message}")

        state['y'] = sol.y[:, -1]
        store_step(sol.t[-1], state['y'])

        if sol.status != 0:  # Check if the integration was successful
            break
    pbar.close()  # Close progress bar

    return result


def compute_shape(out, x1, y1, x2, y2, x3, y3, initial_conditions):
    m1 = initial_conditions['m'][0]
    m2 = initial_conditions['m'][1]
    m3 = initial_conditions['m'][2]

    # Compute Jacobi coordinates
    r1x = (x1 - x2) / math.sqrt(2)
    r1y = (y1 - y2) / math.sqrt(2)
    r2x = ((m1 * x1 + m2 * x2) / (m1 + m2) - x3) * 2 / math.sqrt(6)
    r2y = ((m1 * y1 + m2 * y2) / (m1 + m2) - y3) * 2 / math.sqrt(6)
    r1sq = r1x * r1x + r1y * r1y
    r2sq = r2x * r2x + r2y * r2y

    # Convert to shape space
    out[2] = 2.0 * (r1x * r2y - r1y * r2x) / (r1sq + r2sq)
    out[0] = 2.0 * (r1x * r2x + r1y * r2y) / (r1sq + r2sq)
    out[1] = (r2sq - r1sq) / (r1sq + r2sq)
    return out

print(compute_trajectory(initialConditions, period=initialConditions['period']))