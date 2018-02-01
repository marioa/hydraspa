"""Submodule of included structures and gases

"""

from functools import partial
import glob
from pkg_resources import resource_filename, resource_listdir
import os
import re

_rf = partial(resource_filename, __package__)

def _struc_rf(fn):
    return _rf(os.path.join('structures', fn))

def structure_name(filename):
    try:
        # will strip '_clean' etc from filenames to give CSD reference
        return re.match('^(\w+?)(?:_.+?)?.cif', filename).groups()[0]
    except:
        # some non CSD filenames included in coremof
        return os.path.splitext(filename)[0]

# map structure name to file path
structures = {
    structure_name(fn).upper(): _struc_rf(fn)
    for fn in resource_listdir(__package__, 'structures')
}


def _gas_rf(name):
    return (_rf(os.path.join('gases', name + '.def')),
            _rf(os.path.join('gases', 'pseudo_' + name + '.def')))

gases = {
    nm.upper(): _gas_rf(nm) for nm in ('Ar', 'CO2', 'N2', 'helium')
}


forcefields = {
    'UFF': _rf(os.path.join('forcefields', 'uff.def'))
}
ff_cutoffs = {
    'UFF': 12.8,
}


FRAMEWORK = """\
#CoreShells bond  BondDipoles UreyBradley bend  inv  tors improper-torsion bond/bond bond/bend bend/bend stretch/torsion bend/torsion
          0    0            0           0    0    0     0                0         0         0         0               0            0
"""

INPUT_TEMPLATE = """\
SimulationType                MonteCarlo
NumberOfCycles                100000
NumberOfInitializationCycles  0
PrintEvery                    100
PrintPropertiesEvery          100
RestartFile                   no

# Restart and crash-recovery
# Write a binary file (binary restart.dat).
ContinueAfterCrash              no
# The output frequency of the crash-recovery file.
WriteBinaryRestartFileEvery     0

Forcefield                    %%FFNAME%%
CutOffVDW                     %%CUTOFF%%
ChargeMethod                  Ewald
CutOffChargeCharge            %%CUTOFF%%
EwaldPrecision                1e-6
UseChargesFromCIFFile         yes

Framework 0
FrameworkName %%STRUCTURENAME%%
UnitCells %%NCELLS%%
HeliumVoidFraction 0.78
ExternalTemperature %%TEMPERATURE%%
ExternalPressure    %%PRESSURE%%
Movies no
WriteMoviesEvery    0

# Grids
NumberOfGrids 0

Component 0 MoleculeName             %%GASNAME%%
            TranslationProbability   0.25
            SwapProbability          0.75
            CreateNumberOfMolecules  0
"""
