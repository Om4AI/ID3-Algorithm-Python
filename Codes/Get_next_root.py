# Import libraries
import numpy as np
import pandas as pd
import math
from pprint import pprint


# Function to get the next root node
def get_next_root(df, out_col, positive_attr):
    l = list(df.columns)
    l.remove(out_col)
    
    # Get the root node
    root = ""
    max_infogain = 0
    for attr in l:
        t = cal_information_gain(df, attr, out_col, positive_attr)
        if(t>max_infogain):
            max_infogain =t;
            root = attr
    return root