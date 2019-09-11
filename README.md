# Build Instructions

1. Install Python 3.7.3: https://www.python.org/downloads/release/python-373/
2. Install virtualenv with `$ pip3 install virtualenv`.
3. Create a virtual environment in this directory with `you@host:magtrack$ virtualenv venv`. Activate the virtual environment with `you@host:magtrack$ source venv/bin/activate`.
4. Install dependencies with `(venv) pip install -r req.txt`.

# Run Instructions
1. In the virtual environment, run Main.py with `(venv) you@host:magtrack$ python Main.py path/to/tif/directory` for each image sequence you've collected.
2. Aggregate the cell CSVs into one file with `(venv) you@host:magtrack$ python data_processing.py`.
3. Create separate CSVs by cell type with `(venv) you@host:magtrack$ python cell_type_separation.py`.
4. Plot your data with `(venv) you@host:magtrack$ python plot.py`

# Contents

All data is in the `./Results/` directory. All cell information can be found in `./Results/all_cells.csv`. Cells are also separated by type in `./Results/c1.csv` and `./Results/193.csv`. Individual acquisitions are separated in `./Results/cell_csvs`.
