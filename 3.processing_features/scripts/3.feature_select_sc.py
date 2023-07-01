#!/usr/bin/env python
# coding: utf-8

# # Perform feature selection on normalized merged single cells for each plate

# ## Import libraries

# In[1]:


import sys
import pathlib
import os
import yaml
import json

import pandas as pd
from pycytominer import feature_select
from pycytominer.cyto_utils import output


# ## Set paths and variables

# In[2]:


# output directory for feature selected data
output_dir = pathlib.Path("./data/feature_selected_data")
# if directory if doesn't exist, will not raise error if it already exists
os.makedirs(output_dir, exist_ok=True)

# load in dicionary from yaml file
dictionary_path = pathlib.Path("./plate_info_dictionary.yaml")
with open(dictionary_path) as file:
    plate_info_dictionary = yaml.load(file, Loader=yaml.FullLoader)

# view the dictionary to confirm all info is included to use for normalization
print(json.dumps(plate_info_dictionary, indent=4))


# ## Perform feature selection
# 
# The operations that we are using for feature selection are:
# 
# - `variance_threshold`: creates a list of excluded features that have very low varience of values between single cells
#   
# - `correlation_threshold`: creates a list of excluded features with a correlation to at least one other feature greater than the default threshold (`threshold=0.9`)
#   
# - `blocklist`: creates a list of excluded features using the [standard blocklist file](https://github.com/cytomining/pycytominer/blob/master/pycytominer/data/blocklist_features.txt) for CellProfiler features from Pycytominer
# 
# For more information regarding these operations, please visit [the Pycytominer operations folder](https://github.com/cytomining/pycytominer/tree/master/pycytominer/operations) on GitHub.
# To view how `blocklist` works, please visit [the separate file](https://github.com/cytomining/pycytominer/blob/a5ae6c81a275b692ef5d4c85cfeb37696bf69242/pycytominer/cyto_utils/features.py#L13) for that function.

# In[3]:


# list of operations for feature select function to use on input profile
feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
]

# process each run
for plate, info in plate_info_dictionary.items():
    normalized_df = pd.read_parquet(info["normalized_path"])
    # output_file does not need to be saved to dictionary as there are no more processin steps after this
    output_file = str(pathlib.Path(f"{output_dir}/{plate}_sc_norm_fs.parquet"))
    print(f"Performing feature selection on normalized annotated merged single cells for {plate}!")

    # perform feature selection with the operations specified
    feature_select_df = feature_select(
        normalized_df,
        operation=feature_select_ops,
        output_file="none",
    )

    # save features selected df as parquet file
    output(
        df=feature_select_df,
        output_filename=output_file,
        output_type="parquet"
    )
    print(f"Features have been selected for {plate} and saved!")


# In[4]:


# print last feature selected df to assess if feature selection occurred (less columns)
print(feature_select_df.shape)
feature_select_df.head()

