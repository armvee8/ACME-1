# Sean Wade

import numpy as np
from matplotlib import pyplot as plt
import time
import pysg

def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
    return newfunc

def hat_approximation(f,l):
    """This function will return a list of the correct coefficients to approximate the function f up to level l.
    Parameters
    ----------
        f (function) : The function of a single variable to approximate
        l (int) : The order to use for interpolating the hat function

    Returns
    -------
        coeffs (list) : Entry n is an ndarray of len(2^(n-1)) and contains the coefficients for phi_{nm}.  The length of this should be l.
    """

    def phi(x):
        if abs(x) > 1:
            return 0
        else:
            return 1 - abs(x)

    def phi_ji(j,i,x):
        return phi(2**(j-1)*(x+1) - (2*i) + 1)

    def p_nm(n,m):
        return 2**(2-n)*(m-.5)-1

    coeffs = []
    for n in xrange(1,l+1):
        c_n = np.empty(2**(n-1))
        for m in xrange(1,2**(n-1)+1):
            f_at_p_nm = f(p_nm(n,m))
            for s in xrange(1,n):
                for t in xrange(1, 2**(s-1)+1):
                    f_at_p_nm -= coeffs[s-1][t-1] * phi_ji(s,t,p_nm(n,m))
            c_n[m-1] = f_at_p_nm
        coeffs.append(c_n)
    return coeffs

def integrate_hat(coeffs):

    """Takes a list of coefficients generated by hat_approximation.
    Returns the value of the integral.
    Parameters
    ----------
        coeffs (ndarray) : coefficients generated by hat_approximation
    Returns
    ----------
    Value of the integral
    """
    totalArea = 0
    for i,x in enumerate(coeffs):
        for j in range(len(x)):
            totalArea += coeffs[i][j] * 2 ** (-i)
    return totalArea

    
def prob3():
    """Create and show 2 graphs. One displays error and the other displays 
    execution time.
    """
    f = lambda x: np.sqrt(1-x**2)
    realAnswer = np.pi / 2
    error = []
    timeList = []
    for l in xrange(1,11):
        start = time.time()
        myAnswer = integrate_hat(hat_approximation(f,l))
        end = time.time()
        timeList.append(end - start)
        error.append(abs(realAnswer - myAnswer))
    x_points = range(1,11)
    plt.subplot(121)
    plt.plot(x_points,error)
    plt.title("Error")
    plt.subplot(122)
    plt.plot(x_points, timeList)
    plt.title("Time")
    plt.show()


def prob4():
    """Plot the grid points for a 2-D grid of level 5.
    """
    grid = pysg.sparseGrid(2,5)
    grid.plotGrid()


