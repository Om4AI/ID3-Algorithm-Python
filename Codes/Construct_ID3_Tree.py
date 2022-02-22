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