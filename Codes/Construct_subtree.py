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