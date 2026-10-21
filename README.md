# microyz

**Microdosimetry: lineal energy (y) and specific energy (z) distributions in
liquid water**, computed exclusively with Geant4-DNA physics processes and
models. Author: S. Incerti et al., for the Geant4-DNA collaboration.

---

## 🔬 What this test does

A mono-energetic e- beam is tracked through liquid water using Geant4-DNA
track-structure physics, and the single-event microdosimetric distributions
y (lineal energy) and z (specific energy) are scored and plotted
(`microyz_plot.C`).

## 📚 Reference

- Source: `geant-validation-tests/src/microyz` (Geant4-DNA `microyz` example).
- Geant4-DNA collaboration publications: Phys. Med. 31 (2015) 861-874, and
  further references at http://geant4-dna.org.

## Import notes

- `main.cc`, `include/`, `src/` come from `microyz.cc`/`include`/`src` in
  `geant-validation-tests/src/microyz`.
- `macro/` contains the two visualization macros found directly in that
  source tree (kept for reference, not used by CI — not even
  self-contained), plus 4 concrete macros generated from
  `geant-config-generator`'s own `template.conf`/`params.conf` — see
  `validation/README.md`.
- `validation/parser.py` was **rewritten** for the `metadata()`/`parse()`
  module API that `ci-workflows/validation/export.py` actually calls (the
  first version, copied unmodified from
  `geant-config-generator/tests/geant4/microyz/parser.py`, used the old
  `gts.BaseParser` class API — and shelled out to run a ROOT macro as a
  subprocess, now reproduced directly with `uproot` instead). See
  `validation/README.md` for details. The vendored `gts` package is no
  longer needed and was removed.
