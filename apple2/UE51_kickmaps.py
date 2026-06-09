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
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec
from matplotlib.tri import Triangulation,  CubicTriInterpolator
from shapely.geometry import LineString, point
import time
import radia as rd
import cv2
import os




def plot_kickmap(raw_string, fig_title=None, units='T2m2', energy_gev=None, 
                 log_b2=False, kx_lim=None, ky_lim=None, b2_lim=None):
    """
    Parse and plot a RADIA FldFocKickPer output string.

    Parameters
    ----------
    raw_string : str
        Raw output string from FldFocKickPer (element [5] of return list).
    fig_title : str, optional
        Override figure suptitle. Defaults to device length annotation.
    units : str
        Units label for kick colorbars. Passed through from the RADIA call —
        no conversion is performed here. Typically 'T2m2', 'rad', 'microrad'.
    energy_gev : float, optional
        Beam energy in GeV. Used for annotation only if units are 'rad'/'microrad'.
    log_b2 : bool
        If True, plot B² map on a log colour scale. Useful given the large
        dynamic range (corner/centre ratio can be ~50x).

    Returns
    -------
    fig : matplotlib.figure.Figure
    axes : dict with keys 'kx', 'ky', 'b2', 'lineout'
    data : dict with keys 'x', 'y', 'Kx', 'Ky', 'B2', 'length_m', 'nx', 'ny'
    """

    # ------------------------------------------------------------------
    # 1. Parse
    # ------------------------------------------------------------------
    lines = raw_string.strip().split('\n')

    length_m = float(_get_value_after(lines, '# Undulator Length [m]'))
    nx = int(_get_value_after(lines, '# Number of Horizontal Points'))
    ny = int(_get_value_after(lines, '# Number of Vertical Points'))

    block_starts = [i + 1 for i, l in enumerate(lines) if l.strip() == 'START']
    if len(block_starts) < 3:
        raise ValueError(f"Expected 3 START blocks, found {len(block_starts)}")

    x_axis, y_axis, Kx = _parse_block(lines, block_starts[0])
    _,      _,      Ky = _parse_block(lines, block_starts[1])
    _,      _,      B2 = _parse_block(lines, block_starts[2])

    x_mm = x_axis * 1e3
    y_mm = y_axis * 1e3

    # On-axis lineouts: interpolate y=0 as mean of innermost ±y rows
    # Grid has no y=0 point — rows are symmetric so this is clean
    mid = ny // 2
    kx_onaxis = 0.5 * (Kx[mid - 1, :] + Kx[mid, :])
    ky_onaxis = 0.5 * (Ky[mid - 1, :] + Ky[mid, :])
    b2_onaxis = 0.5 * (B2[mid - 1, :] + B2[mid, :])

    # ------------------------------------------------------------------
    # 2. Layout
    # ------------------------------------------------------------------
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.32)

    ax_kx      = fig.add_subplot(gs[0, 0])
    ax_ky      = fig.add_subplot(gs[0, 1])
    ax_b2      = fig.add_subplot(gs[1, 0])
    ax_lineout = fig.add_subplot(gs[1, 1])

    axes = {'kx': ax_kx, 'ky': ax_ky, 'b2': ax_b2, 'lineout': ax_lineout}

    # ------------------------------------------------------------------
    # 3. Kick maps — diverging colormap, symmetric about zero
    # ------------------------------------------------------------------
    _plot_2d(ax_kx, x_mm, y_mm, Kx,
             title=f'Horizontal Kick $K_x$',
             cbar_label=f'$K_x$ [{units}]',
             cmap='RdBu_r', diverging=True,
             nx=nx, ny=ny, clim = kx_lim)

    _plot_2d(ax_ky, x_mm, y_mm, Ky,
             title=f'Vertical Kick $K_y$',
             cbar_label=f'$K_y$ [{units}]',
             cmap='RdBu_r', diverging=True,
             nx=nx, ny=ny, clim = ky_lim)

    # ------------------------------------------------------------------
    # 4. B² map — sequential, optional log scale
    # ------------------------------------------------------------------
    from matplotlib.colors import LogNorm
    norm = LogNorm(vmin=B2.min(), vmax=B2.max()) if log_b2 else None
    _plot_2d(ax_b2, x_mm, y_mm, B2,
             title=r'$\int B_\perp^2\,\mathrm{d}s$',
             cbar_label=r'$\int B_\perp^2\,\mathrm{d}s$ [T²m]',
             cmap='plasma', diverging=False,
             nx=nx, ny=ny, norm=norm, clim = b2_lim)
    if log_b2:
        ax_b2.set_title(ax_b2.get_title() + '  (log scale)', fontsize=10)

# ------------------------------------------------------------------
    # 5. On-axis lineouts
    # ------------------------------------------------------------------
    colour_kx = '#d62728'
    colour_ky = '#1f77b4'
    colour_b2 = '#2ca02c'

    ax_lineout.axhline(0, color='k', lw=0.5, ls='--', alpha=0.4)
    ax_lineout.plot(x_mm, kx_onaxis, color=colour_kx, lw=1.8,
                    label=f'$K_x$ (y≈0)')
    ax_lineout.plot(x_mm, ky_onaxis, color=colour_ky, lw=1.8,
                    label=f'$K_y$ (y≈0)')
    ax_lineout.set_xlabel('x [mm]')
    ax_lineout.set_ylabel(f'Kick [{units}]', color='k')
    ax_lineout.tick_params(axis='y')
    ax_lineout.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax_lineout.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    ax2 = ax_lineout.twinx()
    ax2.plot(x_mm, b2_onaxis, color=colour_b2, lw=1.4, ls='--',
             label=r'$\int B_\perp^2\,\mathrm{d}s$ (y≈0)')
    ax2.set_ylabel(r'$\int B_\perp^2\,\mathrm{d}s$ [T²m]', color=colour_b2)
    ax2.tick_params(axis='y', labelcolor=colour_b2)
    ax2.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    # -- Lineout axis limits --
    if kx_lim is not None and ky_lim is not None:
        ax_lineout.set_ylim(min(kx_lim[0], ky_lim[0]), max(kx_lim[1], ky_lim[1]))
    elif kx_lim is not None:
        ax_lineout.set_ylim(kx_lim)
    elif ky_lim is not None:
        ax_lineout.set_ylim(ky_lim)

    if b2_lim is not None:
        ax2.set_ylim(b2_lim)

    # Combined legend
    lines1, labels1 = ax_lineout.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax_lineout.legend(lines1 + lines2, labels1 + labels2,
                      fontsize=8, loc='upper right')
    ax_lineout.set_title('On-axis lineouts (y ≈ 0)', fontsize=10)
    ax_lineout.set_xlim(x_mm[0], x_mm[-1])
    ax_lineout.grid(True, alpha=0.25)

    # ------------------------------------------------------------------
    # 6. Annotations and suptitle
    # ------------------------------------------------------------------
    energy_str = f',  E = {energy_gev} GeV' if energy_gev else ''
    default_title = (f'Kick Map  |  L = {length_m*1e3:.1f} mm'
                     f'  |  grid {nx}×{ny}'
                     f'  |  units: {units}{energy_str}')
    fig.suptitle(fig_title or default_title, fontsize=12, y=1.01)

    # Symmetry violation annotation on Kx panel
    kx_asym = np.max(np.abs(Kx + Kx[:, ::-1]))
    ky_asym = np.max(np.abs(Ky + Ky[::-1, :]))
    ax_kx.annotate(f'max antisym. violation: {kx_asym:.1e} {units}',
                   xy=(0.02, 0.03), xycoords='axes fraction',
                   fontsize=7, color='grey')
    ax_ky.annotate(f'max antisym. violation: {ky_asym:.1e} {units}',
                   xy=(0.02, 0.03), xycoords='axes fraction',
                   fontsize=7, color='grey')

    data = dict(x=x_mm, y=y_mm, Kx=Kx, Ky=Ky, B2=B2,
                length_m=length_m, nx=nx, ny=ny)

    return fig, axes, data


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _get_value_after(lines, key):
    for i, l in enumerate(lines):
        if l.strip() == key:
            return lines[i + 1].strip()
    raise ValueError(f"Key not found: {key}")


def _parse_block(lines, start_idx):
    x_vals = np.array(lines[start_idx].split(), dtype=float)
    y_vals, rows = [], []
    for line in lines[start_idx + 1:]:
        s = line.strip()
        if not s or s.startswith('#'):
            break
        vals = np.array(s.split(), dtype=float)
        y_vals.append(vals[0])
        rows.append(vals[1:])
    return x_vals, np.array(y_vals), np.array(rows)


def _plot_2d(ax, x_mm, y_mm, data, title, cbar_label, cmap,
             diverging, nx, ny, norm=None, clim = None):
    if clim is not None:
        vmin, vmax = clim
    elif diverging:
        vmax = np.max(np.abs(data))
        vmin = -vmax
    else:
        vmin, vmax = data.min(), data.max()
        
    levels = np.linspace(vmin, vmax, 64)

    cf = ax.contourf(x_mm, y_mm, data,
                     levels=levels, cmap=cmap,
                     vmin=None if norm else vmin,
                     vmax=None if norm else vmax,
                     norm=norm)
    # Overlay contour lines
    nlines = 7
    cl = ax.contour(x_mm, y_mm, data,
                    levels=np.linspace(vmin, vmax, nlines), colors='k', linewidths=0.4, alpha=0.4,
                    norm=norm)

    # Grid point markers
    xx, yy = np.meshgrid(x_mm, y_mm)
    ax.scatter(xx, yy, s=4, c='k', alpha=0.3, zorder=5)

    cbar = plt.colorbar(cf, ax=ax, pad=0.02)
    cbar.set_label(cbar_label, fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    cbar.formatter = ticker.ScalarFormatter(useMathText=True)
    cbar.formatter.set_powerlimits((0, 0))
    cbar.update_ticks()

    ax.set_xlabel('x [mm]', fontsize=9)
    ax.set_ylabel('y [mm]', fontsize=9)
    ax.set_title(title, fontsize=10)
    ax.set_xlim(x_mm[0], x_mm[-1])
    ax.set_ylim(y_mm[-1], y_mm[0])
    ax.tick_params(labelsize=8)
    ax.set_aspect('auto')
    ax.grid(False)

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

def loopdeloop(gap,shift,shiftmode):
    #parameter_Set Horizontal_polarisation
    rd.UtiDelAll()
    UE51_params = parameters.model_parameters(Mova = 0,
                                        periods = 10, 
                                        periodlength =51.3,
                                        nominal_fmagnet_dimensions = [40.0,0.0,40.0], 
                                        #square_magnet = True,
                                        nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                        #nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                        #nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                        compappleseparation = 75,
                                        apple_clampcut = 6.0,
                                        comp_magnet_chamfer = [3.0,0.0,3.0],
                                        magnets_per_period = 4,
                                        rowtorowgap = 1.2,
                                        gap = 15, 
                                        rowshift = shift,
                                        shiftmode = shiftmode,
                                        block_subdivision = [3,2,1],
                                        M = 1.31,
                                        type = 'Plain_APPLE'                                        
                                        )
    
    
    UE51 = id1.plainAPPLE(UE51_params)
    
    UE51.cont.wradSolve()
    
    fileheader = 'Undulator {}, Gap {}mm, Shift {}mm, Mode {}'.format(UE51_params.periodlength,
                                                                      gap,
                                                                      shift,
                                                                      shiftmode)
    
    a = rd.FldFocKickPer(UE51.cont.radobj, [0,0,0],[0,1,0],51.3,78,[1,0,0],30,61,6,25,'fileheader',[11,50,0,0])#,'T2m2',1.72,'tab')
    with open('D:/Results/UE51/kick_maps/kick_{}l_{}g_{}s_{}m.txt'.format(UE51_params.periodlength,
                                                                      gap,
                                                                      shift,
                                                                      shiftmode), 'w') as f:
        f.write(a[5])
    
    figtitle = 'UE{} ¦¦ Mode: {} ¦¦ Gap: {}mm 11 Shift {}mm'.format(UE51_params.periodlength,
                                                                  shiftmode,
                                                                  gap,
                                                                  shift
                                                                  )
    
    b, c, d = plot_kickmap(a[5], fig_title = figtitle, kx_lim=(-6e-3,6e-3), ky_lim = (-6e-3,6e-3), b2_lim = (0,2))
    
    b.savefig('D:/Results/UE51/kick_maps/kickmap_{}l_{}g_{}s_{}m.png'.format(UE51_params.periodlength,
                                                                      gap,
                                                                      shift,
                                                                      shiftmode), dpi=150, bbox_inches='tight')
    plt.close(b)
    

def makevid(gap, shifts, shiftmode):
    image_folder = 'D:/Results/UE51/kick_maps/'
    video_name = 'UE51_Kicks_{}_mode_{}mm_gap.avi'.format(shiftmode, gap)
    
    
    image_ref = '{}kickmap_51.3l_15g_3.20625s_circularm.png'.format(image_folder)
    frame = cv2.imread(image_ref)
    height, width, layers = frame.shape
    
    video = cv2.VideoWriter(os.path.join(image_folder,video_name),0, 2    , (width,height))
    
    for shift in shifts:
        print(shift)
        image = 'kickmap_{}l_{}g_{}s_{}m.png'.format(51.3,
                                                      gap,
                                                      shift,
                                                      shiftmode)
        frame = cv2.imread(os.path.join(image_folder, image))
        resized_frame = cv2.resize(frame,(width,height))
        print ('I found {}'.format(os.path.join(image_folder, image)))
        video.write(resized_frame)
    
    cv2.destroyAllWindows()
    video.release()

if __name__ == '__main__':
    gaps = np.arange(15,16,2)
    shifts = np.concatenate([[-25.65], np.arange(-25, 26), [25.65]])
#    shifts = np.array([-16*25.65/16])
    shiftmodes = ['linear', 'circular']
    

    
    for shiftmode in shiftmodes:
        for gap in gaps:
            for shift in shifts:
                print('kickin out da kick map for Gap {}, Shift {} in Mode {}'.format(gap, shift, shiftmode))
                loopdeloop(15, shift, shiftmode)
                
        makevid(gaps[0],shifts,shiftmode)
                
    
    
    print(1)