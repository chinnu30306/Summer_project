import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

def angle_between_vectors(u, v):
    dot_product = np.dot(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    cos_theta = dot_product / (norm_u * norm_v)
    return np.degrees(np.arccos(cos_theta))

def straight_line(x, m, c):
    func = m*x + c
    return func

#%%
#read data
data = np.genfromtxt("/Users/chinmayib/Documents/University/Projects/Summer project/ephemeris_data.txt", dtype=str, delimiter="\n")

#initialise arrays
x = np.array([])
y = np.array([])
z = np.array([])
vx = np.array([])
vy = np.array([])
vz = np.array([])
lt = np.array([])
rg = np.array([])
rr = np.array([])

#appending to arrays
i = 1
while i <= len(data):
    if i%4 != 0:
        if i%4 == 1:
            x = np.append(x, float(data[i][3:25]))
            y = np.append(y, float(data[i][29:51]))
            z = np.append(z, float(data[i][55:]))
        elif i%4 == 2:
            vx = np.append(vx, float(data[i][3:25]))
            vy = np.append(vy, float(data[i][29:51]))
            vz = np.append(vz, float(data[i][55:]))
        else:
            lt = np.append(lt, float(data[i][3:25]))
            rg = np.append(rg, float(data[i][29:51]))
            rr = np.append(rr, float(data[i][55:]))
        i += 1
    else:
        i += 1
        continue

#%%
day = np.linspace(0, len(rr), num=len(rr))
peaks, properties = find_peaks(-(rr)) #find minima to get index of perihelion values

a = np.array([x[peaks[1]], y[peaks[1]], z[peaks[1]]])
theta = np.array([])

for j in range(0, len(peaks)):
    b = np.array([x[peaks[j]], y[peaks[j]], z[peaks[j]]])
    theta = np.append(theta, angle_between_vectors(a, b))

#%%
initial_guess = [1, 1]
popt, pcov = curve_fit(straight_line, peaks, theta, p0=initial_guess)
precession = popt[0] * 1.3149e8
precession_unc = np.sqrt(pcov[0][0]) * 1.3149e8
print("Precession rate: ", precession, " +/- ", precession_unc, " arcsec/century")

plt.plot(peaks, theta, '.')
plt.plot(peaks, straight_line(peaks, popt[0], popt[1]))
plt.show()
















