# IDModels Package Audit Report

*A technical review of the IDModels Python package and a plan for returning it to its original goals.*

**Author:** E Rial
**Date:** 2026-06-09
**Version:** 2 (markdown) — original v1 was `IDModels_Audit_Report.docx`

> **What changed in v2.** The report was ported from `.docx` to markdown for easier editing.
> Three findings from v1 were re-diagnosed after re-checking against source (C6, M1, C2 — see
> §11 *Revision Notes*), several missed findings were added, and the Plan of Action (§8) was
> re-sequenced to add a runnable baseline (Step 0), an installable-package prerequisite before
> moving study scripts, and explicit acceptance criteria for the physics work.

---

## 1. Executive Summary

IDModels was created to provide a consistent, traceable, Pythonic interface for specifying
insertion device (ID) magnet models, driving field calculations via the Radia FEM engine
(wrapped by wRadia), and persisting all results — field, integrals, trajectory, K parameter,
and field shape — to well-structured HDF5 files. That goal remains sound and the original
architecture to achieve it is largely present.

Six years of incremental additions, physicist scripting habits, and project-specific one-off
studies have left the repository in a state where:

- The core library code and device-specific study scripts are co-mingled in the same Python package hierarchy.
- The analysis pipeline (integrals, trajectory, K, field shape) is structurally designed but never implemented — key methods are empty stubs or actively broken.
- A second, legacy parameter class exists alongside the canonical one (and is still imported, though dead, by core library code).
- The analysis framework is hard-coupled to a specific device model (`apple2p5/model2.py`), making it device-specific rather than generic.
- Personal machine paths, pickle files, and debugging print statements are embedded in library code.
- The Python environment specification declares Python 2.7 despite the entire codebase requiring Python 3.

This report itemises all findings, prioritises them, and proposes a two-stage recovery plan:
a stabilisation phase (immediate, low-risk fixes) followed by a structured refactor phase that
completes the original design. **The package needs completion, not redesign.**

---

## 2. Background and Original Intent

### 2.1 wRadia

wRadia wraps the Radia C-extension magnet modelling library in Python objects that retain
geometry, material, and magnetisation data in accessible Python attributes, rather than losing
that state into opaque C-level Radia object IDs. The key wrapper objects are:

- `wradObjThckPgn` — a thick-polygon magnet block, holding vertices, magnetisation, material, and colour alongside its Radia ID.
- `wradObjCnt` — a container for wrad objects, propagating spatial and field transforms recursively down the object tree.
- `wradMatLin` — a linear magnetisation material specification.

The effect is that every spatial and field transformation updates both the Radia C-object and
the Python-side state, giving full traceability of where every magnet block is and what its
magnetisation is at any point during model construction. **wRadia is clean and complete; it is
out of scope for this recovery and should not be touched.**

### 2.2 IDModels

IDModels sits on top of wRadia with three responsibilities:

- **Specification** — a single `model_parameters` class capturing all physical parameters of an ID (period length, gap, magnet dimensions, material properties, etc.), serialisable to JSON or HDF5.
- **Construction** — composing wRadia objects into Halbach arrays, terminations, and full device assemblies (plain APPLE, compensated APPLE, CPMU, etc.) from those parameters.
- **Analysis** — running field, integral, trajectory and force calculations over a scan of operating points (gap, shift, phase) and bundling all results into a consistently structured HDF5 file.

The intended output for any device study was a single self-describing HDF5 file containing every
calculated quantity at every operating point, with device parameters stored as attributes, so
the file could be loaded and re-plotted without re-running Radia.

---

## 3. Package Structure Analysis

Current directory tree of importable packages and notable files:

```
IDModels/
├── idcomponents/          # Core reusable building blocks
│   ├── parameters.py      # model_parameters, scan_parameters
│   ├── magnet_shapes.py   # Individual magnet shape classes
│   └── halbach_arrays.py  # Array assembly
├── apple2p5/              # Device assembly models
│   ├── model1.py          # Legacy procedural model (c.2020) — DEPRECATED
│   └── model2.py          # Current OO assembly (plainAPPLE, compensatedAPPLE...)
├── idanalysis/            # Analysis pipeline
│   ├── analysis_functions.py  # CaseSolution, Solution, HyperSolution
│   └── read_plot_write.py     # STUB — never completed
├── test/                  # Unit tests (3 files)
│
├── animation/             # 7 standalone visualisation scripts (not library code)
├── apple2/                # APPLE II device-specific scripts and data files
├── athenaii/              # ATHENA II device scripts and SRI2022 conference figures
├── athenaii_studies/      # 10+ date-stamped study scripts (2021–2025)
├── bessy3/                # BESSY 3 device studies
├── ivue32/                # iVUE32 device studies
├── knot/                  # KNOT device studies
├── tribsapple/            # TRIBS APPLE studies
├── cpmu/                  # CPMU model (March 2026, incomplete)
├── cue17/                 # CUE17 force optimiser
└── reporting/             # Incomplete Word report generator
```

The fundamental structural problem is visible immediately: the importable package namespace
contains both reusable library code (`idcomponents`, `apple2p5/model2`, `idanalysis`) and
device-specific study scripts (`athenaii_studies`, `apple2`, `bessy3`, etc.) at the same level.
There is no distinction between "reusable tool" and "one-off study script that happened to be
committed." Everything is importable; nothing is documented as stable API versus exploratory code.

---

## 4. Core Component Review

### 4.1 idcomponents/parameters.py — model_parameters

The architectural spine of the package, and well conceived. The keyword-defaults pattern
(`prop_defaults` dict + `kwargs.get`) is clean and extensible. Derived attributes are correctly
computed in `__init__`. The `save()`/`load()` JSON methods exist.

Issues identified:

- `h5.special_dtype()` (line 22) is from an old h5py API and is deprecated. Replace with `h5py.string_dtype()`.
- TODO at line 173 (`def read json / write json / write to h5 / read h5`) — HDF5 persistence was always intended but only JSON exists. The write-to-h5 method is still missing.
- `load()` re-hardcodes `coordinate_names` as `['X','S','Z']` (line 206), discarding any value stored in the JSON file.
- `save()` serialises the `wradMatLin` magnet_material by replacing it with `[ksi, M]` — fragile; any attribute that is not an ndarray or wradMatLin will raise `TypeError` in `json.dump`. Add explicit type guards.
- **(New in v2)** `save()` does `tmp_dict = vars(self)` — that is the *live* `__dict__`, not a copy — then mutates it (arrays → lists, material → list). **Calling `save()` corrupts the in-memory object.** Copy first.
- The square-magnet logic (lines 129–133) is asymmetric: it sets fmagnet and cmagnet dimensions but not hcmagnet/vcmagnet, which are independently sized for compensated APPLEs.
- `magnet_profile` (line 139) defaults to `np.random.rand(...)`. A random default is almost certainly wrong — a flat profile should be the default.
- The derived `rows` attribute (lines 152–158) only handles a subset of device types — see Q9 and the related device-type-string defect (§4.5).

### 4.2 idcomponents/magnet_shapes.py

The class hierarchy is the right approach: each shape is a class, construction fully driven by
`model_parameters`. The APPLE clamp-cut implementation (three polygon pieces) matches the physical
geometry correctly.

Issues identified:

- **`cpmuMagnet` (line 460) is a verbatim copy of `appleMagnet`** with a TODO "NEEDS making CPMU magnet 19.3.2026". It is not a CPMU magnet; using it produces geometrically incorrect CPMU results.
- `appleMagnetFELr4`/`appleMagnetFELr6` have hardcoded magic numbers (1.58, 3.0) embedded in polygon corners — should be parameters.
- **`appleMagnetNonSymmetric` has a confirmed bug**: in p1's polygon (lines 93–94) the z-coordinates use `nominal_fmagnet_dimensions[0]` where the first two corners use `[2]`, mixing transverse and vertical dimension references for an asymmetric magnet.
- `HcompMagnet` and `VcompMagnet` are near-identical — candidate for a single parameterised class.
- `tribsAppleMiddleMagnet` contains ~10 lines of commented-out alternative polygon definitions. Remove.
- The `__main__` block (line 511) runs Radia solve + interactive plot — inappropriate for a library module.

### 4.3 idcomponents/halbach_arrays.py

The class-based approach (`HalbachArray`, `HalbachTermination_APPLE`, etc.) is the right design.
The `perturbation_fn` mechanism (injection of alignment errors) is a mature feature. `MagnetRow`
correctly encodes beam, quadrant, and row metadata.

Issues identified:

- **Import defect at line 16: `from apple2p5.model1 import model_hyper_parameters`.** Core library importing a specific device's legacy class. **(Corrected in v2)** This import is in fact *dead* — the name `model_hyper_parameters` is shadowed in every `__init__` by the parameter of the same name (default `parameters.model_parameters()`), so the imported class is never referenced. The correct fix is to **delete line 16** (no replacement needed). It still matters: the statement creates an import-time dependency on `model1.py`, so the module breaks if `model1.py` is removed.
- `HalbachArray`, `HalbachArrayCompensation`, and `Halbach2Array` contain an identical `array_number` selection block. Extract to a helper.
- `per_length` is set in that block but never used in `HalbachArray`/`HalbachArrayCompensation`. Dead code.
- `Halbach2ArrayTermination` (line 208) is an empty stub. Dead code.
- `HalbachTermination_APPLE_HZB` has fractional magic numbers (31/32, 7/32, 9/32, 3/32) encoding design ratios — name them or comment the design reference.
- The `__main__` block (line 362) tests with hardcoded period length and `rd.ObjDrwOpenGL` — misleading in a library file.

### 4.4 apple2p5/model1.py vs apple2p5/model2.py

`model1.py` is the original 2020 procedural code with a local `model_hyper_parameters` class.
`model2.py` refactored this to the current OO approach (`plainAPPLE`, `compensatedAPPLEv2`, etc.)
using the canonical `model_parameters`.

Issues:

- `model1.py` should be deprecated and removed. Its only consumers are the (now dead) import in `halbach_arrays.py` and `test_ATHENA_Model.py`. The tests reference `appleUpperBeam`/`appleArray`, which exist only in `model1.py` — so the test suite tests legacy code, not the current code.
- `model1.py`'s `model_hyper_parameters` uses different attribute names from `model_parameters` (`applePeriods` vs `periods`, `mainmagdimension` vs `nominal_fmagnet_dimensions`, `clampcut` vs `apple_clampcut`). Two live vocabularies create confusion.
- Two long, identical commented-out `BfieldStreamPlot` bodies (~80 lines each) at the end of `compensatedAPPLEv2` and `compensatedAPPLEv2_Sym`. Delete.
- `compensatedAPPLEv1` uses the old dict-based `self.allarrays` approach (no beam/quadrant/row metadata). It is the only remaining user of the old approach — remove or update.

### 4.5 idanalysis/analysis_functions.py

The most important file for the stated goals, and the one in worst shape relative to them. The
design — `CaseSolution` (single operating point), `Solution` (scanned parameters), `HyperSolution`
(scanned design parameters) — is sound and clearly the intended top-level API.

**Critical issues:**

- **Hard coupling to a device model:** `from apple2p5 import model2 as id` (line 23). `Solution.solve()` directly instantiates `id.plainAPPLE`, `id.compensatedAPPLEv2`, etc. New device types cannot be analysed without editing the framework. (See §8.2 step 2.2 — the fix is more than a factory; the *model interface contract* must be defined.)
- **Integral / field / torque calculations are not implemented:** `calculate_first_integral()`, `calculate_second_integral()`, `calculate_H_Field()`, `calculate_M_field()`, and all `calculate_torque_*()` are stubs. **(Corrected in v2)** They are *not* uniformly `pass` — `calculate_first_integral()` contains broken code (`for x in range(plane)` with `plane=[]` → `TypeError`), so requesting `'Integrals'` *crashes* rather than no-ops. The stated primary purpose of the package is unimplemented.
- **Personal machine path** hardcoded as a default argument in `Solution.save()` (line 524: `'M:\Work\Athena_APPLEIII\Python\Results\\'`). Default-argument paths evaluate at import time and fail on any other machine.
- The `__main__` block uses pickle for intermediate storage (lines 1038–1039) despite HDF5 being the design target. Pickle is not portable or self-describing.
- `results['Bprofile']` is hardcoded to shape `[..., 1001, 4]` (line 366) and `results['1st_Integral']` to `[..., 81, 2]` (line 379). These magic numbers should derive from `scan_parameters`.
- `MetaData` (line 27) hardcodes `facility = 'Helmholtz Zentrum Berlin'` and `IDType = 'Compensated APPLE'` as fixed values, not defaults.
- `tracemalloc`, `time`, `random`, `itertools`, `copy`, `pickle`, `pandas`, `plotly` are all imported at module top. Memory tracing, dataframes and interactive plotting have no place in a physics calculation library.

**Minor issues:**

- `print(1)` at line 110 (inside the broken integral loop) and line 450; `print("You ain't plotted anything yet!")` in `Solution.plot()` (line 552). Debugging residue.
- **(Corrected in v2 — was C6)** `HyperSolution.solve()` calls `self.extract_hyper_results(tmp_sol)` after the loop. v1 called this "uses only the last solution." In fact **`extract_hyper_results(self, solution)` never references its `solution` argument** — it operates on `self.solutions` (all of them). So the argument is dead and misleading, not a last-only bug. The *real* defects in this area are: (a) the dead parameter, (b) fragile `np.reshape` + `np.ndenumerate` accumulation logic, and (c) the `scan_parameters == 'default'` branch (line 610) referencing `test_hyper_params`, a name that only exists in `__main__` → guaranteed `NameError`.
- **(New in v2)** The `Solution.__init__` `'Torques'` branch references `self.magnet_rows` (lines 420, 426), which does not exist (should be `self.hyper_params.magnet_rows`). The entire Torques path is untested dead code.
- **(New in v2) Device-type-string mismatch.** `parameters.py` sets `rows`/`magnet_rows` only for `'Compensated_APPLE'`, `'Symmetrically Compensated APPLE'`, `'Plain_APPLE'`. But `Solution.solve()` branches on `'Anti-symmetrically Compensated APPLE'`, which matches *neither* — so `rows` is never set and every force calculation for that type raises `AttributeError`. (Q9 understated this as `rows=0`; it is actually undefined/crash.)
- `CaseSolution.calculate_force_per_magnet()` (lines 141–150) does deeply nested index arithmetic directly on the internal wRadia `objectlist` with magic indices. Brittle.

### 4.6 idanalysis/read_plot_write.py

A short stub containing only a `WrdPlotObject` class whose `__init__` creates a matplotlib figure
and does nothing with it. Never developed. Given the name implies the standardised HDF5
read/write/plot pipeline, this is a significant gap.

---

## 5. Scope Creep: Device Study Scripts

The following directories live *inside* the importable package but contain device-specific or
conference-specific scripts rather than reusable library code:

| Directory | Contents | Assessment |
|---|---|---|
| `animation/` | 7 scripts incl. `test1-3.py` | Standalone animation scripts. `test1-3.py` clearly temporary. |
| `apple2/` | `UE49.py`, `UE51.py`, shimming/measurement scripts, `.npy` data | Device studies + data files (`babs_demo.npy`, `bphi_demo.npy`) that should not be in the package. |
| `athenaii/` | `SRI2022/figures*.py` | Conference figure scripts. |
| `athenaii_studies/` | 10 date-stamped scripts (2021–2025), `bunny.py`, `ipac2025_analysis.py` | A research lab notebook committed to the repo. The most egregious scope creep. |
| `bessy3/` | 6 scripts incl. `ImpactOnFluxBrill.py`, `cryo_apple.py` | BESSY3-specific design studies. |
| `ivue32/` | 3 scripts incl. `plottingfromhdf5.py` | Device-specific. `plottingfromhdf5.py` may contain reusable HDF5 read logic worth salvaging. |
| `knot/` | `studies20250318.py` | Single KNOT study. |
| `tribsapple/` | `first_draft.py` | Incomplete TRIBS APPLE draft. |
| `cue17/` | `force_optimiser.py` | Device-specific force optimisation. |
| `reporting/` | `sandbox.py`, example `.docx`/`.png`/`.json` | Incomplete report generator + binary artefacts that should not be in version control. |

All of the above should be moved **outside the importable package namespace**. The strongly
preferred target (see §8) is a **separate repository** (`HZB_ID_Studies/`) that imports IDModels
as an installed dependency — treating IDModels like any external library you do not edit to make
a study work.

A secondary effect of mixing studies into the package: they import `analysis_functions.py`
directly and pass device-specific parameters in, which has created pressure to expand
`analysis_functions.py` to handle more device types — directly feeding the coupling problem in §4.5.

---

## 6. Testing Infrastructure

| File | Tests | Quality assessment |
|---|---|---|
| `test_ATHENA_Model.py` | 6 magnet-orientation tests for `appleUpperBeam` | Tests legacy `model1.py`, not `model2.py`. Accesses magnetisation via raw `objectlist` index chains (implementation details, not API). Imports `wradia as wrd` at package level. |
| `test_MagnetsAndArrays.py` | Magnet shapes / arrays (not deeply reviewed) | Exists; content not verified. |
| `test_analysis_functions.py` | 1 real test asserting `cont.radobj == 1` | Tests that a Radia object was created, not any physics. `SetUp` is misspelled (capital U) so the fixture never runs. Uses `magnets_per_period=6` (non-standard). No field values tested. |

The CI pipeline (GitHub Actions, Docker) is structurally well set up. But with one trivially-passing
real test and the analysis pipeline mostly unimplemented, **CI passing is not meaningful assurance
of correctness.**

`environment.yml` specifies `python=2.7`. The codebase requires Python 3 (f-strings, `print()`
function). The conda environment described by this file cannot run the code.

---

## 7. Complete Issues List (Prioritised)

Severity/diagnosis updated in v2 where noted.

### 7.1 Critical — fix before any further development

| # | Issue | Location |
|---|---|---|
| C1 | `analysis_functions.py` imports `apple2p5.model2` directly, coupling analysis to a specific device. New models cannot be analysed without editing the framework. | `idanalysis/analysis_functions.py:23` |
| C2 | Integral/field/torque calculations are stubs; `calculate_first_integral()` is *actively broken* (crashes on call). Core purpose unimplemented. | `analysis_functions.py:95–330` |
| C3 | `read_plot_write.py` is a stub. Standardised HDF5 read/write is not implemented. | `idanalysis/read_plot_write.py` |
| C4 | `environment.yml` specifies `python=2.7`. The environment is non-functional. | `environment.yml` |
| C5 | `cpmuMagnet` is a copy-paste of `appleMagnet` with a TODO. Geometrically incorrect for CPMU. | `idcomponents/magnet_shapes.py:460` |
| C6 | **(Re-scoped in v2)** `HyperSolution` result-aggregation is unreliable: `extract_hyper_results` ignores its argument, the reshape/ndenumerate logic is fragile, and the `scan_parameters=='default'` branch raises `NameError`. *Not* the "last-solution" bug described in v1. | `analysis_functions.py:610, 763, 765` |

### 7.2 Major — resolve in first refactor phase

| # | Issue | Location |
|---|---|---|
| M1 | **(Corrected in v2)** `halbach_arrays.py` imports `model_hyper_parameters` from `apple2p5.model1`. The import is *dead* (shadowed) — delete line 16; no replacement needed. Still removes an import-time dependency on legacy code. | `idcomponents/halbach_arrays.py:16` |
| M2 | Two parameter classes (`model_hyper_parameters` in model1, `model_parameters` in parameters.py). Both reachable; should be one. | `apple2p5/model1.py`, `idcomponents/parameters.py:18` |
| M3 | `test_ATHENA_Model.py` tests `model1.py` (legacy), not `model2.py`. Tests do not cover the code in use. | `test/test_ATHENA_Model.py` |
| M4 | Personal path `M:\Work\...` hardcoded as a default argument in `Solution.save()`. | `analysis_functions.py:524` |
| M5 | All device study scripts live inside the importable namespace. | `athenaii_studies/`, `apple2/`, `bessy3/`, `ivue32/`, `knot/`, `tribsapple/`, `cue17/` |
| M6 | Binary files (`.docx`, `.png`, `.npy`) committed to the repo. | `reporting/`, `apple2/` |
| M7 | `compensatedAPPLEv1` uses old dict-based array management. Remove or update. | `apple2p5/model2.py` |
| M8 | `appleMagnetNonSymmetric` polygon p1 uses `nominal_fmagnet_dimensions[0]` where `[2]` is expected, mixing transverse/vertical dimensions. | `idcomponents/magnet_shapes.py:93-94` |
| M9 | **(New in v2)** `parameters.save()` mutates the live object `__dict__` (`vars(self)`), corrupting the in-memory object on save. | `idcomponents/parameters.py:181` |
| M10 | **(New in v2)** Device-type strings used by `Solution.solve()` (`'Anti-symmetrically Compensated APPLE'`) do not match those that set `rows` in `parameters.py` → `AttributeError` in force calcs. Single source of truth needed for device-type identifiers. | `parameters.py:152`, `analysis_functions.py:470-480` |

### 7.3 Moderate — quality and maintainability

| # | Issue | Location |
|---|---|---|
| Q1 | Identical `array_number` selection block copy-pasted across three Halbach classes. Extract a helper. | `halbach_arrays.py` |
| Q2 | `Halbach2ArrayTermination` empty stub. Dead code. | `halbach_arrays.py:208` |
| Q3 | `per_length` set but never used. | `halbach_arrays.py` |
| Q4 | `HcompMagnet`/`VcompMagnet` near-identical. Parameterise into one class. | `magnet_shapes.py:157-239` |
| Q5 | Magic numbers (1.58, 3.0) for FEL cut geometry hardcoded in polygons. | `magnet_shapes.py:285-342` |
| Q6 | Large identical commented-out `BfieldStreamPlot` blocks. Delete. | `apple2p5/model2.py` |
| Q7 | `tracemalloc`, `pandas`, `plotly` imported at top of a physics module. | `analysis_functions.py:1-20` |
| Q8 | `magnet_profile` default is `np.random.rand(...)`. Should be flat. | `parameters.py:139` |
| Q9 | `model_parameters.rows` only handles some device types (see M10). New/other types get no `rows` → crash. | `parameters.py:152-158` |
| Q10 | `h5.special_dtype(vlen=str)` deprecated. Use `h5py.string_dtype()`. | `parameters.py:22` |
| Q11 | `MetaData` hardcodes facility/IDType as fixed values. | `analysis_functions.py:27` |
| Q12 | Debugging residue: `print(1)`, plot message. | `analysis_functions.py:110, 450, 552` |
| Q13 | `testCaseSolution` asserts `cont.radobj==1`, not physics. | `test/test_analysis_functions.py` |
| Q14 | `SetUp` (capital U) so pytest/unittest never runs it as a fixture. | `test/test_analysis_functions.py` |
| Q15 | `animation/` contains `test1-3.py` — not production code. | `animation/` |

---

## 8. Plan of Action

Two phases. **Phase 0** establishes a runnable, tested baseline (added in v2 — you cannot safely
refactor code you cannot execute). **Phase 1** is low-risk stabilisation that does not change the
external interface. **Phase 2** completes the original design layer by layer.

Rough effort weighting: Phase 0 is hours; Phase 1 is ~1–2 days of low-risk edits; the entire
weight and the only domain-sensitive work is Phase 2 steps 2.3–2.5. Do not treat the step lists
as equal-sized items.

### 8.0 Phase 0: Establish a runnable baseline (do this first)

| Step | Task |
|---|---|
| 0.1 | Pick **one** canonical install path. The repo has `environment.yml`, `requirements.txt`, `setup.py`, and a `Dockerfile` with no documented entry point. Choose one, document it in the README, and confirm `import idcomponents`, `import idanalysis`, `import apple2p5.model2` all succeed. |
| 0.2 | Get the existing test suite running (`pytest`), even though most tests are trivial or test legacy code. A green-or-known-red baseline is the regression net for everything that follows. |
| 0.3 | Make IDModels **installable as an editable package** (`pip install -e .` via `setup.py`/`pyproject.toml`). This is a prerequisite for Step 1.8 (moving studies out) — study scripts must be able to `import idmodels...` once they no longer live inside the tree. |

### 8.1 Phase 1: Stabilise

Order below minimises merge risk; individual steps are largely independent.

| Step | Task | Ref | Risk |
|---|---|---|---|
| 1.1 | Fix `environment.yml`: `python=2.7` → `python=3.x` matching runtime. Drop `plotly`/`pandas`/`vtk` as core deps (they are not physics deps). Reconcile against the canonical install chosen in 0.1. | C4 | Low |
| 1.2 | Remove the personal path from `Solution.save()`; default to a plain filename or require the caller to pass a path. | M4 | Low |
| 1.3 | **Delete** line 16 of `halbach_arrays.py` (the dead `model1` import). No replacement import is needed — verify nothing references `model_hyper_parameters` at module scope. | M1 | Low |
| 1.4 | Replace `h5.special_dtype(vlen=str)` with `h5py.string_dtype()`. | Q10 | Low |
| 1.5 | Fix `magnet_profile` default: `np.random.rand(...)` → `np.zeros(...)`/`np.ones(...)`. | Q8 | Low |
| 1.6 | Fix `parameters.save()` to copy before mutating (`tmp_dict = dict(vars(self))` or build a fresh dict) so saving cannot corrupt the live object. | M9 | Low |
| 1.7 | Remove debugging prints (`print(1)` ×2, plot message). | Q12 | Low |
| 1.8 | Fix `test_analysis_functions.py`: rename `SetUp`→`setUp`; assert a field *value*, not just `radobj` ID. | Q13, Q14 | Low |
| 1.9 | **Move all study directories out of the package** (`athenaii_studies`, `apple2`, `bessy3`, `ivue32`, `knot`, `tribsapple`, `cue17`, `animation`, plus `reporting/` artefacts). Preferred: a separate `HZB_ID_Studies/` repo depending on the editable install from 0.3. Minimum acceptable: a top-level `studies/` directory outside the importable namespace. Fix the moved scripts' imports against the installed package. Add `.gitignore` rules for binary/data files. | M5, M6 | Medium |
| 1.10 | Guard `cpmuMagnet` to raise `NotImplementedError` on instantiation, preventing silently incorrect CPMU calculations until the real shape exists (2.7). | C5 | Low |
| 1.11 | Delete `Halbach2ArrayTermination` (empty stub) and the dead `per_length` variables. | Q2, Q3 | Low |

> **Sequencing note:** 1.9 depends on Phase 0 (the package must be installable before studies can be moved and re-imported). Do not attempt 1.9 before 0.3.

### 8.2 Phase 2: Structured completion

| Step | Task | Ref |
|---|---|---|
| 2.0 | **Define a validation reference *before* implementing any physics** (new in v2). Pick at least one known case with an analytic or previously-trusted answer: ideal-Halbach peak field, `K = 0.0934·λ[mm]·B[T]`, or a trusted prior Radia result for one device. This is the oracle that lets you distinguish a correct integral from a plausible-looking wrong one. Without it, 2.3–2.5 cannot be verified. | C2 |
| 2.1 | Consolidate parameter classes. Map old `model_hyper_parameters` names (`applePeriods`, `mainmagdimension`, `clampcut`) to `model_parameters` equivalents. Remove `model1.py` (or relegate to studies). Update `test_ATHENA_Model.py` to test `model2.py` with `model_parameters`. Establish a single source of truth for device-type identifier strings (fixes M10). | M2, M3, M10 |
| 2.2 | Decouple analysis from device model. **Define the explicit interface a "model" must expose** — `.cont.radobj`, `.model_parameters`, `.allarraytabs` with `.row`/`.quadrant`/`.beam`, `.rownames` — and have `Solution.solve()` accept a `model_factory` callable conforming to it. Injecting the constructor alone is insufficient while `CaseSolution` reaches into model internals; the contract is the deliverable. Remove the `apple2p5.model2` import. | C1 |
| 2.3 | **Lock the HDF5 save→load→plot pipeline on the quantities that already work (B field, forces) first** (re-sequenced in v2). Complete `read_plot_write.py` and `model_parameters` HDF5 persistence against real B/force data, with a round-trip test. This validates the output format before new physics is added, so integrals slot into a proven pipeline rather than stacking two unknowns. | C3 |
| 2.4 | Implement `calculate_first_integral()` and `calculate_second_integral()` (replace the broken loop). Use `rd.FldInt` over a grid; store as 2D arrays (position vs integral); save to HDF5; validate against the 2.0 reference. Derive array shapes from `scan_parameters`, not magic numbers. | C2 |
| 2.5 | Implement on-axis trajectory and K parameter; integrate field numerically for the electron trajectory; derive K from peak transverse field and period length; validate against 2.0. | C2 |
| 2.6 | Build the real CPMU magnet shape and device model (using `Halbach2Array` for hybrid geometry); replace the `NotImplementedError` guard from 1.10. | C5 |
| 2.7 | Extract duplicate `HcompMagnet`/`VcompMagnet` into one parameterised class; extract the shared `array_number` selection logic in `halbach_arrays.py` into a helper. | Q1, Q4 |
| 2.8 | Add field-shape / harmonics output to `CaseSolution` (normalised field profile, leading harmonics) — part of the original stated goal. | C2 |
| 2.9 | Expand test coverage: magnet orientations on `model2.py`, field integrals returning values within tolerance of the 2.0 reference, `model_parameters` serialisation round-trip. | M3 |

---

## 9. Target Architecture (After Recovery)

Arrows indicate "depends on." After recovery, no arrows point upward.

```
  HZB_ID_Studies/      (separate repo — device scripts; NOT part of the package)
      │  (imports IDModels as an installed dependency)
      ▼
  idanalysis/          (Solution, HyperSolution, CaseSolution, read_plot_write)
      │
      ▼
  apple2p5/model2      (plainAPPLE, compensatedAPPLE, tribsAPPLE, cpmu)
  cpmu/cpmu_hzb        (also at this level)
      │
      ▼
  idcomponents/        (parameters, magnet_shapes, halbach_arrays)
      │
      ▼
  wRadia               (wrad_obj, wrad_mat)
      │
      ▼
  radia                (C extension)
```

Currently `analysis_functions.py` violates this by importing `apple2p5/model2.py` directly
(C1), and `halbach_arrays.py` carries a dead import of `apple2p5/model1.py` (M1) — an inverted
dependency arrow that disappears once line 16 is deleted.

---

## 10. Summary of Findings

| Category | Count | Priority |
|---|---|---|
| Critical issues | 6 | Fix before further development |
| Major issues | 10 | Phase 1 (+ 2.1) |
| Quality / maintainability issues | 15 | Phase 1–2 cleanup |
| Study-script directories inside the namespace | 9 | Move out in Phase 1 (after Phase 0) |

The original design of IDModels is sound. `model_parameters`, the wRadia-based component
hierarchy, and the `CaseSolution`/`Solution`/`HyperSolution` framework are the right abstractions.
The issues are correctness problems, incomplete implementations, and accumulated physicist-scripting
habits — not fundamental architectural mistakes.

**Highest-leverage structural change:** Step 1.9 — getting study scripts out of the package
namespace (which depends on Phase 0 making the package installable). This makes the structure
legible and stops the pattern of coupling analysis code to specific devices.

**Most important functionality gap:** Steps 2.4–2.5 — field integrals, trajectory and K with
standardised HDF5 output — gated by the validation reference defined in 2.0. Without these the
package does not fulfil its primary stated purpose.

---

## 11. Revision Notes (v1 → v2)

Findings re-checked against source; changes from the original `.docx`:

- **C6 re-scoped.** v1: "`HyperSolution.solve()` uses only the last solution." Reality: `extract_hyper_results` ignores its argument entirely and operates on `self.solutions`; the genuine defects are the dead parameter, the fragile reshape/ndenumerate aggregation, and a `NameError` in the `scan_parameters=='default'` branch.
- **M1 corrected.** The legacy `model1` import in `halbach_arrays.py` is *dead* (shadowed by a same-named parameter). Fix is deletion, not substitution; v1's proposed replacement import would itself be unused.
- **C2 sharpened.** The integral methods are not uniformly `pass`; `calculate_first_integral()` is actively broken and raises on call.
- **Added M9** — `parameters.save()` corrupts the live object via `vars(self)`.
- **Added M10 / sharpened Q9** — device-type strings used in `Solution.solve()` do not match those that set `rows` in `parameters.py`, causing `AttributeError` rather than `rows=0`.
- **Noted** the `'Torques'` branch references a non-existent `self.magnet_rows`.
- **Plan:** added **Phase 0** (runnable baseline + editable install), made Step 1.9 (move studies) depend on it, recommended a *separate studies repo* over an in-repo `studies/` folder, added **Step 2.0** (validation reference before physics), expanded **Step 2.2** to require defining the model interface contract, and **re-sequenced** HDF5 pipeline work (2.3) ahead of the integrals so the output format is locked and tested on already-working quantities first.
