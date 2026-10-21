#!/usr/bin/env python

# microyz portal parser: metadata() reads the macro, parse() the "yz"
# TNtuple (radius, eventID, nbHits, nbScoredHits, y, z, Einc) written to
# yz.root, computing the population-weighted mean lineal energy yF.
#
# Ported from geant-config-generator/tests/geant4/microyz/parser.py
# (gts.BaseParser, which shelled out to `root -l -b -q microyz_plot.C(...)`
# to post-process the ROOT ntuple, merging repeated-seed job groups into one
# multi-energy curve) to the module-level metadata()/parse() API expected by
# ci-workflows/validation/export.py. The yF computation from
# microyz_plot.C is reproduced directly with uproot (no ROOT binary, no
# PyROOT on the runner — consistent with LowEFrag/TestEm12-DPK in this
# organization); there is no job-group merge any more — one macro means one
# run, so each macro now yields its own single-point chart instead of the
# original's multi-energy curve (see validation/README.md).
import os

from geantval import getJSON, one_command, single_run


def metadata(commands):
    single_run(commands)
    energy, unit = one_command(commands, "/gun/energy").split()
    if unit != "keV":
        raise ValueError("Expected a keV beam energy, got: " + unit)
    return {"TEST": "microyz",
            "PHYSLIST": one_command(commands, "/microyz/phys/addPhysics"),
            "PARTICLE": one_command(commands, "/gun/particle"),
            "ENERGY_EV": float(energy) * 1000.}


def compute_yF(path):
    import uproot

    with uproot.open(path) as root:
        ntuple = root["yz"]
        arrays = ntuple.arrays(["nbHits", "nbScoredHits", "y"], library="np")

    population = 0.
    yF_anal = 0.
    for hits, scored, y in zip(arrays["nbHits"], arrays["nbScoredHits"], arrays["y"]):
        weight = hits / scored
        population += weight
        yF_anal += weight * y
    if population == 0.:
        raise ValueError("No scored hits found in " + path)
    return yF_anal / population


def parse(job):
    yF = compute_yF(os.path.join(job["path"], "yz.root"))

    rjson = getJSON(job, "chart",
                     mctool_name="GEANT4",
                     mctool_model=job["PHYSLIST"],
                     observableName="microdosimetry y",
                     targetName="Water",
                     beamParticle=job["PARTICLE"],
                     beamEnergies=[job["ENERGY_EV"]],
                     title="microdosimetry y",
                     xAxisName="E (eV)",
                     yAxisName="y (keV/um)",
                     xValues=[job["ENERGY_EV"]],
                     yValues=[yF])
    yield rjson
