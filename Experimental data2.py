import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def straight_line(x, m, c):
    func = m*x + c
    return func

#%%
#read data
data = np.genfromtxt("/Users/chinmayib/Documents/University/Projects/Summer project/horizons_results.txt", dtype=str, delimiter="\n")

#initialise arrays
om = np.array([])
w = np.array([])

#appending to arrays
i = 1
while i <= len(data):
    if i%5 != 0:
        if i%5 == 2:
            om = np.append(om, float(data[i][3:25]))
            w = np.append(w, float(data[i][29:51]))
        i += 1
    else:
        i += 1
        continue

#%%
day = np.linspace(0, len(w), num=len(w))
theta = om + w

initial_guess = [4.37e-6, 77.4]
popt, pcov = curve_fit(straight_line, day, theta, p0=initial_guess)
precession = popt[0] * 1.3149e8
precession_unc = np.sqrt(pcov[0][0]) * 1.3149e8
print("Precession rate: ", precession, " +/- ", precession_unc, " arcsec/century")

plt.plot(day, theta)
plt.plot(day, straight_line(theta, popt[0], popt[1]))
plt.show()


