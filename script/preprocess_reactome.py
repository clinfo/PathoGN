fp=open("reactome_db.graph.tsv","w")
for line in open("03data_graph/reactome.graph.tsv"):
    arr=line.strip().split("\t")
    if len(arr)==3:
        el1=arr[0].split("|")
        el2=arr[2].split("|")
        if len(el1)==1 and len(el2)==1:
            fp.write(line)
        else:
            for e1 in el1:
                for e2 in el2:
                    s="\t".join([e1,arr[1],e2])
                    fp.write(s)
                    fp.write("\n")
    else:
        print("ERROR")

