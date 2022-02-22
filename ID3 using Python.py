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
            max_infogain =t
            root = attr
    return root


# Function to get nodes and their corresponding final decisions
def get_decisions(df, attr, out_col, positive_attr):
    dec_dict = {}
    subattrs = list(df[attr].value_counts().index)
    subattrs_occ = list(df[attr].value_counts().values)
    for i in range(len(subattrs)):
        sub_attr = subattrs[i]
        occ = subattrs_occ[i]
        yes_occ = df[(df[attr]==sub_attr) & (df[out_col]==positive_attr)].shape[0]
        if(yes_occ==occ):
            dec_dict[sub_attr] = "Yes"
        elif((occ-yes_occ)==occ):
            dec_dict[sub_attr] = "No"
        else: dec_dict[sub_attr] = "?"
    return dec_dict


# Recursive function to construct subtree
def construct_subtree(k, root, df, out_col, positive_attr):
    
    # Create new dataset
    dff = df[df[root]==k]
    dff = dff.drop(root, axis=1)
    
    temp_root = get_next_root(dff, out_col, positive_attr)
#     print("Root: ", root," || Subroot: ",temp_root)
    temp_dict = get_decisions(dff, temp_root, out_col, positive_attr)
#     print("Dictionary for current subroot: ", temp_dict, "\n")
    f=1
    for key in temp_dict.keys():
        if(temp_dict[key]=='?'):
            f = 0
            temp_dict[key] = construct_subtree(key, temp_root, dff, out_col, positive_attr)
#             print("Key: ",key, temp_dict[key])
    temp_dict["Root"] = temp_root
    return temp_dict



# Function to display the ID3 Decsion Tree
def draw_tree(d, root_spaces, root):
    if(d["Root"]!=root):
        buffer = math.ceil(1/len(d['Root']))*3
        print((" "*(root_spaces+4)),d["Root"])
    else: print((d["Root"]))
    for k in d.keys():
        if(k=="Root"):continue
        elif(k!="Root" and (d[k]=="Yes" or d[k]=="No")):
            print(("  "*root_spaces),k," --> ",d[k])
        else:
            print(("  "*root_spaces), k, "-->")
            draw_tree(d[k], root_spaces+5, root)


# Final Function to construct & display full tree
def construct_ID3_tree(data_file, index_col, out_col, positive_attr, root_spaces):
    # Extract data
    df = get_data(data_file, index_col)
    
    # Final decision tree dictionary
    id3_tree = {}
    
    # Get root node
    root = get_next_root(df,out_col,positive_attr)
    id3_tree = get_decisions(df,root, out_col,positive_attr)
    
    for k in id3_tree.keys():
        if(id3_tree[k]=='?'):
            # Create a subtree
            id3_tree[k] = construct_subtree(k, root ,df, out_col, positive_attr)
    id3_tree['Root'] = root
    draw_tree(id3_tree, root_spaces, id3_tree["Root"])
    return id3_tree