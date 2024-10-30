import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import math
import sys 
from IPython.display import Image
from scipy.optimize import curve_fit

######### Manning #########

def calculate_Manningcoefficient(R, S, v): 
    n = (1/v) * R**(2/3) * S**(1/2)
    return n


def calculate_discharge_Manning(A, n, R, S):
    Q = A * (1/n) * R**(2/3) * S**(1/2)
    return Q

def calculate_velocity_Manning(n, R, S):
    v = (1/n) * R**(2/3) * S**(1/2)
    return v


######### Leopold & Maddock #########

def calculate_multipliers_Leopold_Method1(b, f, m, w, d, v, Q): 
    a = []
    c = []
    k = []
    for i in range(len(w)): 
        a = w / Q**b
        c = d / Q**f
        k = v / Q**m
    a_mean = a.mean()
    c_mean = c.mean()
    k_mean = k.mean()
    return a_mean, c_mean, k_mean

def check_Leopold_parameters(width, depth, velocity, Q, b, f, m, a, c, k, tol):         #NOG NIET AF
    Q_Leopold = width * depth * velocity
    powers = b + f + m
    multipliers = a * c * k
    
    # Check tolerance
    Q_check = np.isclose(Q_Leopold, Q, rtol=tol)
    powers_check = np.isclose(powers, 1, rtol=tol)
    multipliers_check = np.isclose(multipliers, 1, rtol=tol)
    
    return Q_check, powers_check, multipliers_check


def calculate_Leopold_discharge(width, depth_average, velocity_average, a, c, k, b, f, m): 
    Q_width = (width / a)**(1/b)
    Q_depth = (depth_average / c)**(1/f)
    Q_velocity = (velocity_average / k)**(1/m)
    
    Q_average = (Q_width + Q_depth + Q_velocity) / 3
    return Q_width, Q_depth, Q_velocity, Q_average