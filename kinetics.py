from scipy.integrate import solve_ivp
import numpy as np

# the maximum time of virus in days
maxtime = 365

# people in Idaho
N = 1787065  # Idaho population estimate for July 1, 2019 from
# https://www.census.gov/quickfacts/ID


def kinetics(k1, k2, S_0, I_0, R_0):  # Units of k1
    def abc(t, y):
        """ System of differential equations: y(t) = [S(t),I(t),R(t)]
            returns:
                A list containing [dS/dt, dI/dt, dR/dt]
        """
        # Susceptible, Infected, Recovered
        S, I, R = y
        return [
                -k1 * S * I / (S + I + R),
                k1 * S * I / (S + I + R) - k2 * I,
                k2 * I
                ]

    return solve_ivp(
        abc,
        [0, maxtime],
        [S_0, I_0, R_0],
        t_eval=np.arange(0, maxtime, 1),
        method="Radau",
        dense_output=True,
    )
