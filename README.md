# Build Instructions

1. Install Python 3.7.3: https://www.python.org/downloads/release/python-373/
2. Install virtualenv with `$ pip3 install virtualenv`.
3. Create a virtual environment in this directory with `you@host:magtrack$ virtualenv venv`. Activate the virtual environment with `you@host:magtrack$ source venv/bin/activate`.
4. Install dependencies with `(venv) pip install -r req.txt`.

# Run Instructions
1. In the virtual environment, run Main.py with `(venv) you@host:magtrack$ python Main.py path/to/tif/directory`.

# Contents

All data is in the `./Results/` directory. All cell information can be found in `./Results/all_cells.csv`. Cells are also separated by type in `./Results/c1.csv` and `./Results/193.csv`. Individual acquisitions are separated in `./Results/cell_csvs`.
