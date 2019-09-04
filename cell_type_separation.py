# Copyright 2019 Johanan Idicula
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd

cell_beads_data = pd.read_csv("./Results/all_cells.csv")

cell_beads_193_boolean = cell_beads_data.cell_type.str.contains('193')
cell_beads_193 = cell_beads_data[cell_beads_193_boolean]
cell_beads_193.to_csv("./Results/193.csv")

cell_beads_c1_boolean = cell_beads_data.cell_type.str.contains('c1')
cell_beads_c1 = cell_beads_data[cell_beads_c1_boolean]
cell_beads_c1.to_csv("./Results/c1.csv")
