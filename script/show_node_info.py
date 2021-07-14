##
## python show_node_info.py --input result/node_info.json --input_node ./sample_kg_nodes1.json --key result/cv_info1.json
##
import json
import sklearn
import sklearn.metrics
import numpy as np
import argparse 
import re

class NumPyArangeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist() # or map(int, obj)
        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    ##
    ## コマンドラインのオプションの設定
    ##
    parser = argparse.ArgumentParser(description = "Classification")
    parser.add_argument("--input",default="result/node_info.json",
        help = "result/cv_info.json", type = str)
    parser.add_argument("--input_node",default="sample_kg_nodes1.json",
        help = "result/cv_info.json", type = str)
    parser.add_argument("--key",default="result/config.1.json",
        help = "result/cv_info.json", type = str)
    parser.add_argument('--output_json',default=None,
        help = "output: json", type=str)
    parser.add_argument('--output_csv',default=None,
        help = "output: csv", type=str)
    parser.add_argument('--output_node_info',default=None,
        help = "output: json", type=str)
    args = parser.parse_args()
    np.random.seed(20)

    filename=args.input
    ifp = open(filename, 'r')
    info=json.load(ifp)
    print("#info",len(info))

    filename=args.input_node
    ifp = open(filename, 'r')
    node_names=json.load(ifp)
    print("#node_name",len(node_names))

    if args.output_csv:
        filename=args.output_csv
        fp = open(filename, 'w')
        fp.write("Graph-Node-ID,CHR,Nuc-Pos,REF-Nuc,ALT-Nuc,Label,GCN-SCORE\n")
        for data in info[args.key]:
            i=int(data[0])
            name=node_names[i]
            m=re.match(r'^(.+)_(\d+)_([ATGC])_([ATGC])$',name)
            if not m:
                print("[ERROR]", name)
            arr=[data[0],m[1],m[2],m[3],m[4],data[1],data[2][1]]
            fp.write(",".join(map(str,arr)))
            fp.write("\n")

    if args.output_node_info:
        print("[SAVE]",args.output_node_info)
        fp = open(args.output_node_info, "w")
        json.dump(all_node_info,fp, indent=4, cls=NumPyArangeEncoder)

