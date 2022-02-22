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