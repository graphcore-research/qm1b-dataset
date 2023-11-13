# QM1B dataset

[![arXiv](https://img.shields.io/badge/arXiv-2311.01135-b31b1b.svg)](https://arxiv.org/abs/2311.01135)
[![QM1B figshare+](https://img.shields.io/badge/figshare%2B-24459376-blue)](https://doi.org/10.25452/figshare.plus.24459376)

QM1B is a low-resolution DFT dataset generated using [PySCF IPU](https://github.com/graphcore-research/pyscf-ipu). It is composed of one billion training examples containing 9-11 heavy atoms. It was created by taking 1.09M SMILES strings from the [GDB-11 database](https://zenodo.org/record/5172018) and computing molecular properties (e.g. HOMO-LUMO gap) for a set of up to 1000 conformers per molecule.

This repository contains utilities for accessing the QM1B dataset but not the raw data as that is stored elsewhere.

## License

Code in this repository is covered by the [MIT license](./LICENSE.md)

The QM1B dataset was generated with 
[pyscf-ipu](https://github.com/graphcore-research/pyscf-ipu) by using the 
[GDB-11 database](https://doi.org/10.5281/zenodo.7041051) as an input and hasn't otherwise
altered the GDB-11 database
The QM1B dataset is made available under the [Creative Commons 4.0 license](./LICENSE-dataset).

## Download

Prepare your python environment:
```bash
pip install -r requirements.txt
```

Run the automated download script
```bash
python download.py  /path/for/qm1b-dataset 
```

## Dataset schema
See the [QM1B datasheet](./DATASHEET.md) for detailed documentation following the [datasheets for datasets](https://doi.org/10.48550/arXiv.1803.09010) framework.

QM1B dataset is stored in the [open-source columnar Apache Parquet format](https://parquet.apache.org/), with the following schema:
* `smile`: The SMILES string taken from GDB11. There are up to 1000 rows (i.e. conformers) with the same SMILES
string.
* `atoms`: String representing the atom symbols of the molecule, e.g. ”COOH”.
* `z`: Integer representation of `atoms` used by SchNet (the atomic numbers).
* `energy`: energy of the molecule computed by PySCF IPU (unit eV).
* `homo`: The energy of the Highest Occupied Molecular Orbital (HOMO) (unit eV).
* `lumo`: The energy of the Lowest occupied Molecular Orbital (LUMO) (unit eV).
* `N`: The number of atomic orbitals for the specific DFT computation (depends on the basis set STO3G).
* `std`: The standard deviation of the energy of the last five iterations of running PySCFIPU, used as
convergence criteria std < 0.01 (unit eV).
* `y`: The HOMO-LUMO Gap (unit eV).
* `pos`: The atom positions (unit Bohr).

## Dataset exploration

Dataset exploration can easily done using Pandas library. For instance, to load the validation set:
```python
import pandas as pd

# 20m entries in the validation set.
print(pd.read_parquet("qm1b_val.parquet").head())
```

## Cite
Please use the following citation for the QM1B dataset

```
@inproceedings{mathiasen2023qm1b,
  title={Generating QM1B with PySCF $ \_ $\{$$\backslash$text $\{$IPU$\}$$\}$ $},
  author={Mathiasen, Alexander and Helal, Hatem and Klaeser, Kerstin and Balanca, Paul and Dean, Josef and Luschi, Carlo and Beaini, Dominique and Fitzgibbon, Andrew William and Masters, Dominic},
  booktitle={Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track},
  year={2023}
}
```
