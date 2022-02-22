# Import libraries
import numpy as np
import pandas as pd
import math
from pprint import pprint

# Function to get Data
# Import dataset and create df
def get_data(file, index_col):
    df = pd.read_csv(file, index_col=index_col)
    return df


# Function to calculate Entropy
def calculate_entropy(attr, df, out_col, positive_attr):
    if(attr=="DS"):
        # Get count of yes and no to get probability
        yes = df[out_col].value_counts()[0]
        no = df[out_col].value_counts()[1]
        p_yes = yes/df.shape[0]
        p_no = no/df.shape[0]
        entropy_ds = -1*((p_yes*math.log2(p_yes))+(p_no*math.log2(p_no)))
        return entropy_ds
    else:
        # Any other attribute's entropy calculation
        attrs = df[attr].value_counts().index
        vals  = df[attr].value_counts().values
        entropy_attr = 0
        for i in range(len(attrs)):
            sub_attr = attrs[i]
            total_occ = vals[i]
            p_sub_attr = total_occ/df.shape[0]
            
            # +ve & -ve occurences of sub-attribute
            sub_yes_occ = df[(df[attr]==sub_attr) & (df[out_col]==positive_attr)].shape[0]
            sub_no_occ = total_occ-sub_yes_occ
            
            # Probability of sub-attribute
            p_sub_yes = sub_yes_occ/total_occ
            p_sub_no = sub_no_occ/total_occ
            if(p_sub_yes==0 and p_sub_no==0):
                entropy_sub = 0
            elif(p_sub_yes==0):
                entropy_sub = -1*((p_sub_no*math.log2(p_sub_no)))
            elif(p_sub_no==0):
                entropy_sub = -1*((p_sub_yes*math.log2(p_sub_yes)))
            else:
                entropy_sub = -1*((p_sub_yes*math.log2(p_sub_yes))+(p_sub_no*math.log2(p_sub_no)))
                
            # Total entropy value updation
            entropy_attr+= (p_sub_attr*entropy_sub)
        return entropy_attr


# Information Gain Function
def cal_information_gain(parent_df, child_attr, out_col, positive_attr):
    # Call entropy function on the full dataset - Parent entropy
    entropy_parent = calculate_entropy("DS", parent_df, out_col, positive_attr)
    
    # Get current child attribute's entropy
    entropy_child = calculate_entropy(child_attr, parent_df, out_col, positive_attr)
    return entropy_parent-entropy_child