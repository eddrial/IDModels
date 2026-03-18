'''
Created on 8 Oct 2025

@author: oqb
'''

import numpy as np
import matplotlib.pyplot as plt
import h5py as h5

def fourier_series_coeffs(t, f, N):
    """
    Compute Fourier series coeffs up to N for periodic data f(t) over one period.
    Uses convention: f(t) ≈ a0/2 + Σ_{n=1..N} [ a_n cos(n ω0 t) + b_n sin(n ω0 t) ].
    """
    T = t[-1] - t[0]
    w0 = 2*np.pi / T
    a0 = (2.0/T) * np.trapz(f, t)
    a = np.zeros(N+1)  # a[0] unused except for readability
    b = np.zeros(N+1)
    for n in range(1, N+1):
        a[n] = (2.0/T) * np.trapz(f * np.cos(n*w0*t), t)
        b[n] = (2.0/T) * np.trapz(f * np.sin(n*w0*t), t)
    return a0, a, b, w0

def reconstruct(t, a0, a, b, w0):
    N = len(a)-1
    f_rec = np.full_like(t, a0/2.0, dtype=float)
    for n in range(1, N+1):
        f_rec += a[n]*np.cos(n*w0*t) + b[n]*np.sin(n*w0*t)
    return f_rec

if __name__ == "__main__":
    # Example "sine-like" curve (periodic over [0, 2π]):
    fname = 'S:/Ed/Measurements/UE51/UE51 Magnetic Measurements/UE51_Final_Gaps.h5'
    T = 2*np.pi
    t = np.linspace(0, T, 2000, endpoint=False)
    with h5.File(fname, "r") as f:
        a = f['UE51']['Undulator']['UE51']['measurement 3']['Analysed Data']['B_array'][:]
        #f = 1.2*np.sin(t) + 0.3*np.sin(3*t + 0.5) + 0.1*np.cos(2*t)  # your data could replace this
    

    N = 10  # number of harmonics to keep
    a0, a, b, w0 = fourier_series_coeffs(t, f, N)
    f_rec = reconstruct(t, a0, a, b, w0)

    # Print first few coefficients
    print(f"a0 = {a0:.6f}")
    for n in range(1, N+1):
        print(f"n={n:2d}: a[{n}]={a[n]: .6f}, b[{n}]={b[n]: .6f}")

    # Compare original vs reconstruction
    plt.figure()
    plt.plot(t, f, label="original")
    plt.plot(t, f_rec, "--", label=f"reconstructed (N={N})")
    plt.legend()
    plt.xlabel("t")
    plt.ylabel("f(t)")
    plt.title("Fourier series reconstruction")
    plt.show()