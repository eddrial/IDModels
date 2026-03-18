'''
Created on 4 Jan 2022

@author: oqb
'''
import numpy as np
from wradia import wrad_obj as wrd
import apple2p5.model2 as id1
from idcomponents import parameters
from idanalysis import analysis_functions as af
from idanalysis.analysis_functions import Solution
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation,  CubicTriInterpolator
from shapely.geometry import LineString, point
import time


import numpy as np

def stokes_from_single_period_field(
    field_1period: np.ndarray,
    harmonic: int = 1,
    window: str = "hann",
    detrend: bool = True,
    transverse_cols: tuple[int, int] = (1, 3),  # (Bx_col, Bz_col) in your input
    s_col: int = 0,
    return_debug: bool = False,
    # ---- fixes / clarifications ----
    map_B_to_E: bool = True,
    # Beam along +s: v × B gives acceleration, so (Bz -> Ex) and (Bx -> Ey) up to sign.
    # If you want the old (incorrect-for-planar) behaviour, set map_B_to_E=False.
    s3_sign: float = -1.0,
    # s3_sign lets you flip the circular-pol sign convention: use -1 (default) or +1.
    verbose: bool = False,
):
    """
    Drop-in: estimate *idealised* Stokes parameters from ONE undulator period of a magnetic field sample.

    Input
    -----
    field_1period : ndarray shape (N, 4)
        Columns: [s, Bx, Bs, Bz] where:
          - s  : coordinate along electron beam axis (monotonic)
          - Bx : horizontal magnetic field component
          - Bs : longitudinal field component (ignored here)
          - Bz : vertical magnetic field component

    What this returns
    -----------------
    Estimates an *idealised* on-axis polarisation state using the complex fundamental of the
    central-period field. By default it uses a physically motivated proxy mapping for a beam
    travelling along +s:

        Ex_proxy ~ fundamental(Bz)
        Ey_proxy ~ fundamental(Bx)

    (Because a ~ v×B, and the radiation E-field follows the transverse acceleration.)

    Then computes Stokes parameters:

        S0 = |Ex|^2 + |Ey|^2
        S1 = |Ex|^2 - |Ey|^2
        S2 = 2 Re(Ex Ey*)
        S3 = s3_sign * 2 Im(Ex Ey*)   (default s3_sign=-1 gives S3 = -2 Im(...))

    Notes / caveat
    --------------
    Bounded idealisation:
      - ignores end fields, full trajectory, finite acceptance, spectral mixing, partial polarisation
      - Bs is ignored

    Conventions
    -----------
    - Propagation is assumed along +s (downstream).
    - Axes: x=horizontal, z=vertical in your field file; we map to (Ex, Ey) via v×B.
    - If your local helicity sign convention differs, set s3_sign=+1.

    """
    arr = np.asarray(field_1period, dtype=float)
    if arr.ndim != 2 or arr.shape[1] < 4:
        raise ValueError("field_1period must be a 2D array with at least 4 columns: [s, Bx, Bs, Bz].")

    s = arr[:, s_col].copy()
    bx = arr[:, transverse_cols[0]].copy()  # horizontal B
    bz = arr[:, transverse_cols[1]].copy()  # vertical B

    if len(s) < 8:
        raise ValueError("Need at least ~8 samples per period to get a sensible fundamental estimate.")
    if not (np.all(np.isfinite(s)) and np.all(np.isfinite(bx)) and np.all(np.isfinite(bz))):
        raise ValueError("Input contains NaN/Inf.")

    # Ensure increasing s
    order = np.argsort(s)
    s, bx, bz = s[order], bx[order], bz[order]

    # Detrend (remove DC offsets)
    if detrend:
        bx = bx - np.mean(bx)
        bz = bz - np.mean(bz)

    n = bx.size

    # Windowing
    wname = "none" if window is None else str(window).lower()
    if window is None or wname == "none":
        w = np.ones(n)
    elif wname == "hann":
        w = np.hanning(n)
    elif wname == "hamming":
        w = np.hamming(n)
    else:
        raise ValueError("window must be one of: None/'none', 'hann', 'hamming'.")

    # Complex Fourier coefficient at the chosen harmonic (record assumed to be one period)
    m = np.arange(n)
    phasor = np.exp(-1j * 2.0 * np.pi * harmonic * m / n)

    # ---- FIX #1: correct B->E proxy mapping for beam along +s ----
    if map_B_to_E:
        Ex = np.sum((bz * w) * phasor)  # vertical B -> horizontal acceleration -> Ex
        Ey = np.sum((bx * w) * phasor)  # horizontal B -> vertical acceleration -> Ey
    else:
        # old behaviour (generally not what you want for planar vertical-field undulators)
        Ex = np.sum((bx * w) * phasor)
        Ey = np.sum((bz * w) * phasor)

    # Stokes (unnormalised)
    S0 = (np.abs(Ex) ** 2 + np.abs(Ey) ** 2)
    S1 = (np.abs(Ex) ** 2 - np.abs(Ey) ** 2)
    S2 = (2.0 * np.real(Ex * np.conj(Ey)))
    # ---- FIX #2: make S3 sign convention explicit and configurable ----
    S3 = (float(s3_sign) * 2.0 * np.imag(Ex * np.conj(Ey)))

    # Normalised
    if S0 == 0:
        s1 = s2 = s3 = np.nan
    else:
        s1, s2, s3 = S1 / S0, S2 / S0, S3 / S0

    # Derived angles (optional)
    psi = 0.5 * np.arctan2(S2, S1)                 # linear angle (rad)
    chi = 0.5 * np.arcsin(np.clip(s3, -1.0, 1.0))  # ellipticity angle (rad)

    out = {
        "S0": float(S0), "S1": float(S1), "S2": float(S2), "S3": float(S3),
        "s1": float(s1), "s2": float(s2), "s3": float(s3),
        "psi_deg": float(np.degrees(psi)),
        "chi_deg": float(np.degrees(chi)),
        "convention_note": (
            f"Assumes propagation along +s. Using map_B_to_E={map_B_to_E} "
            f"(default maps Bz->Ex, Bx->Ey via v×B proxy). "
            f"S3 computed as S3 = {s3_sign:+g} * 2 * Im(Ex*conj(Ey)). "
            "Only an idealised central-period estimate (no ends/trajectory/acceptance)."
        ),
    }

    if return_debug:
        out["debug"] = {
            "Ex_proxy": Ex, "Ey_proxy": Ey,
            "amp_ratio_|Ey|/|Ex|": float(np.abs(Ey) / (np.abs(Ex) + 1e-30)),
            "dphi_rad_arg(Ey)-arg(Ex)": float(np.angle(Ey) - np.angle(Ex)),
            "samples": int(n),
            "window": wname,
            "harmonic": int(harmonic),
            "map_B_to_E": bool(map_B_to_E),
        }

    # ---- FIX #3: don't print by default (library-friendly) ----
    if verbose:
        print("Absolute Stokes parameters:")
        print(f"S0={out['S0']:.6g}, S1={out['S1']:.6g}, S2={out['S2']:.6g}, S3={out['S3']:.6g}")
        print("Normalised:")
        print(f"s1={out['s1']:+.6f}, s2={out['s2']:+.6f}, s3={out['s3']:+.6f}")
        print(f"psi={out['psi_deg']:+.3f}°, chi={out['chi_deg']:+.3f}°")

    return out

def enphitable(enrange,phirange,X,Y):
    
    fig2, ax2 = plt.subplots()
    
    #t0 = time.time()
    
    ax2.tricontour(X.flatten(),Y.flatten(),bphi[0].flatten(), [-89.99])
    ax2.tricontour(X.flatten(),Y.flatten(),E[0].flatten(), [200])
    
    res_table = np.zeros((2,len(enrange),len(phirange),4))
    
    for mode in range(2): #0 is circular, 1 is linear
        for en in range(len(enrange)):
            ax2.tricontour(X.flatten(),Y.flatten(),E[mode].flatten(), [enrange[en]])
            E_contour = ax2.collections[-1]._paths[0].vertices
            l2 = LineString(E_contour)
            for phi in range(len(phirange)):
                ax2.tricontour(X.flatten(),Y.flatten(),bphi[mode].flatten(), [phirange[phi]])
                bphi_contour = ax2.collections[-1]._paths[0].vertices
                l1 = LineString(bphi_contour)
                p = l1.intersection(l2)
                print('For mode {}, at Energy {} and angle {}, phase is expected to be {}, gap is expected to be {}'.format(['circular','linear'][mode], enrange[en],phirange[phi],p.centroid.x,p.centroid.y))
                res_table[mode][en][phi]=[enrange[en],phirange[phi],p.centroid.x,p.centroid.y] #energy,angle, gap, shift 
            
    return res_table

if __name__ == '__main__':
    #define parameter space
    #gaps = np.array([15,17,20,25,30,40,50])
    gaps = np.arange(14,60.1,1)
    shifts = np.arange(-25.65-25.65/16,25.75+25.65/16,25.65/16)
    
    #shifts = np.arange(0,3,4)
    shiftmodes = ['circular', 'linear']
    #shiftmodes = ['linear']
    #set up APPLE 2 device (UE56)
    #solve peakfield in parameter space
    print (gaps)
    print(shifts)
    
    min_gap = 15
    
    #parameter_Set Horizontal_polarisation
    UE51_params = parameters.model_parameters(Mova = 0,
                                        periods = 15, 
                                        periodlength =51.3,
                                        nominal_fmagnet_dimensions = [40.0,0.0,40.0], 
                                        #square_magnet = True,
                                        nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                        #nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                        #nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                        compappleseparation = 75,
                                        apple_clampcut = 5.0,
                                        comp_magnet_chamfer = [3.0,0.0,3.0],
                                        magnets_per_period = 4,
                                        rowtorowgap = 1.2,
                                        gap = 17, 
                                        rowshift = -15.65,
                                        shiftmode = 'circular',
                                        block_subdivision = [3,2,1],
                                        M = 1.31,
                                        type = 'Plain_APPLE'                                        
                                        )
    
    basescan = parameters.scan_parameters(51.3,gaprange = gaps,shiftrange = shifts, shiftmoderange = shiftmodes)
    
    UE51 = id1.plainAPPLE(UE51_params)
    
    UE51.cont.wradSolve()
    
    case = af.CaseSolution(UE51)
    case.calculate_B_field()
    
    print ("Peak Field for ID {} is {}".format('UE51', np.max(case.bmax)))
    
    a = stokes_from_single_period_field(case.bfield)
    
    print('stokes parameters are:\n')
    print({k: a[k] for k in ["s1", "s2", "s3", "psi_deg", "chi_deg"]})
    
    sol = Solution(UE51_params,basescan,property = ['B'])
    
 #   sol.solve('B')
    
 #   babs = np.linalg.norm(sol.results['Bmax'], axis = 3)
 #   bz = sol.results['Bmax'][:,:,:,0]
 #   bx = sol.results['Bmax'][:,:,:,2]
 #   bx[0,:,-2]= 0
 #   bx[0,:,1] = 0
 #   np.save('D:/Results/UE51/babs_UE51_gap_more321.npy',babs)
  #  np.save('D:/Results/UE51/bx_UE51_gap_more321.npy',bx)
  #  np.save('D:/Results/UE51/bz_UE51_gap_more321.npy',bz)
    
    
#    bphi = np.sign(shifts[:]) * (180 / np.pi) * np.arctan(sol.results['Bmax'][:,:,:,0]/sol.results['Bmax'][:,:,:,2])
#    bphi[:,:,1]=-90.1
#    bphi[:,:,-2]=90.1
#    np.save('D:/Results/UE51/bphi_UE51_gap_more321.npy',bphi)
    
    #or load
    bphi=np.load('D:/Results/UE51/bphi_UE51_gap_more321.npy')
    babs=np.load('D:/Results/UE51/babs_UE51_gap_more321.npy')
    bx = np.load('D:/Results/UE51/bx_UE51_gap_more321.npy')
    bz = np.load('D:/Results/UE51/bz_UE51_gap_more321.npy')
    
    bphi[:,:,1]=-90.1
    bphi[:,:,-2]=90.1
    
    
    Kx = 0.0934 * 51.3 * bx
    Kz = 0.0934 * 51.3 * bz
    #lamb = (51.3/(2*4892*4892))*(1 + (Kx*Kx/2)+ (Kz*Kz/2))
    lamb = (51.3/(2*3369*3369))*(1 + (Kx*Kx/2)+ (Kz*Kz/2))
    
    E = 6.626e-34 * 3e8/(1e-3 * lamb*1.6e-19)
    
    X,Y =  np.meshgrid(shifts,gaps)
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    
    ax.plot_surface(X,Y,babs[0])
    
    fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
    
    ax1.plot_surface(X,Y,bphi[0])
    
    fig11, ax11 = plt.subplots(subplot_kw={"projection": "3d"})
    
    ax11.plot_surface(X,Y,E[0])
    
    
    #creating triangular grid, and interpolating (shift, gap)
    #grid creation
    triObj = Triangulation(X.flatten(),Y.flatten())
    
    #cubic interpolation of abs B
    babs_fzc = CubicTriInterpolator(triObj,babs[0].flatten())
    
    bx_fzc = CubicTriInterpolator(triObj,bx[0].flatten())
    
    bz_fzc = CubicTriInterpolator(triObj,bz[0].flatten())
    
    #cubic interpolation of E
    E_fzc = CubicTriInterpolator(triObj,E[0].flatten())
    
    #cubic interpolation of phi
    bphi_fzc = CubicTriInterpolator(triObj,bphi[0].flatten())
    
    #export 100 random values
    
#    rands = np.zeros([100000,4])
#    for i in range(100000):
#        gaprand = 15 + 44* np.random.random()
#        shiftrand = -26 + 52 * np.random.random()
#        rands[i] = [gaprand, shiftrand, E_fzc(shiftrand,gaprand),bphi_fzc(shiftrand,gaprand)]
    
    #plot rands
#    figrand, axrand = plt.subplots()
    
#    axrand.tricontour(rands[:,1],rands[:,0],rands[:,2])
#    axrand.tricontour(rands[:,1],rands[:,0],rands[:,3])
    
    
    enrange = np.arange(240,241)
    phirange = np.arange(-90,90.1,5)
    
    a = enphitable(enrange,phirange,X,Y)
    
    #plot on plane
    fig2, ax2 = plt.subplots()
    
    t0 = time.time()
    
    ax2.tricontour(X.flatten(),Y.flatten(),bphi[0].flatten(), [-89.99])
    ax2.tricontour(X.flatten(),Y.flatten(),E[0].flatten(), [200])
    

    #ax2.tricontour(X.flatten(),Y.flatten(),bphi[0].flatten())
    #ax2.tricontour(X.flatten(),Y.flatten(),babs[0].flatten())
    
    if ax2.collections[0].get_paths().__len__() >= 1:
        bphi_contour = ax2.collections[0]._paths[0].vertices
        l1 = LineString(bphi_contour)
    
    if ax2.collections[1].get_paths().__len__() >= 1:
        E_contour = ax2.collections[1]._paths[0].vertices
        l2 = LineString(E_contour)
        
    if 'l1' in globals() and 'l2' in globals():
        p = l1.intersection(l2)
    
        if isinstance(p,point.Point):
            ax2.plot(p.coords.xy[0],p.coords.xy[1],'ro')
    t1 = time.time()
    print(t1-t0)
    plt.show()
    print(p.coords.xy)
    print('working on points in a loop')
    E_at_H = np.array([124,155.6,191.6,231.1,271.8,313.1,353,388.8,420.2,446.6,468.3,485.4,499.1,509,523.4,531.6])
    E_at_H = np.arange(100,105)
    E_at_V = np.array([157,196,234,269,302,342,379,412,439,487,505,534])
    E_at_magic = np.arange(65,521,1./15.)
    res_table = np.zeros((len(E_at_magic),4))
    for en in range(len(E_at_H)):
        ax2.tricontour(X.flatten(),Y.flatten(),E[0].flatten(), [E_at_H[en]])
        E_contour = ax2.collections[-1]._paths[0].vertices
        l2 = LineString(E_contour)
        p = l1.intersection(l2)
        print('At Energy {} and angle {}, phase is expected to be {}, gap is expected to be {}'.format(E_at_H[en],0,p.coords.xy[0][0],p.coords.xy[1][0]))
        res_table[en] =[0.0,E_at_H[en],p.coords.xy[1][0],p.coords.xy[0][0]] #angle, energy, gap, shift 
    print(res_table)
#    np.savetxt('D:/Results/UE51/magic_angle/g_s_table_0.txt',res_table, header = 'Angle, Energy, Gap, Shift', fmt = '%10.4f')
    