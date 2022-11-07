from numpy import exp, sqrt, pi

def standard_normal(x):
    return (1/sqrt(2 * pi)) * exp((-.5 * (x ** 2)))

def bivariat_normal_dist(x, y):
    pass