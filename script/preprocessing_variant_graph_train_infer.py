import numpy as np
import os
import json
import joblib
import argparse

def load_graph(filenames):
    label_data={}
    nodes=set()
    edges=set()
    label_count={}
    for filename in filenames:
        print("[LOAD]",filename)
        temp_base, ext = os.path.splitext(filename)
        base, data_type = os.path.splitext(temp_base)
        if data_type==".graph":
            for line in open(filename):
                arr=line.strip().split("\t")
                if len(arr)==2:
                    if arr[0]!=arr[1]:
                        edges.add((arr[0],"",arr[1]))
                    else:
                        print("[skip self-loop]",arr[0])
                    nodes.add(arr[0])
                    nodes.add(arr[1])
                elif len(arr)==3:
                    if arr[0]!=arr[2]:
                        edges.add((arr[0],arr[1],arr[2]))
                    else:
                        print("[skip self-loop]",arr[0])
                    nodes.add(arr[0])
                    nodes.add(arr[2])
                else:
                    print("[ERROR] unknown format")
        elif data_type==".label":
            for line in open(filename):
                arr=line.strip().split("\t")
                if len(arr)>=2:
                    label_data[arr[0]]=arr[1]
                    if arr[1] not in label_count: label_count[arr[1]]=0
                    label_count[arr[1]]+=1
                    nodes.add(arr[0])
    return edges, nodes, label_data, label_count

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', nargs='*', default=[], type=str, help='set train dataset')
    parser.add_argument('--infer', nargs='*', default=[], type=str, help='set infer dataset')
    parser.add_argument('--other', nargs='*', default=[], type=str, help='graph components other than train/infer')
    parser.add_argument('--multilabel', action='store_true')
    parser.add_argument('--class_weight','-w', action='store_true')
    parser.add_argument('--multiedge', action='store_true')
    parser.add_argument('--num_label_thresh','-n', type=int, default=0, help='data path')
    parser.add_argument('--output', type=str, default="dataset.jbl", nargs='?', help='save jbl file')
    parser.add_argument('--output_node', type=str, default="nodes_dataset.json", nargs='?', help='save json file')
    parser.add_argument('--uselabels','-u', type=str, default=None, nargs='+',
                        help='label_list_{train,infer}=[nodenum, np.nan] for nodes with labels not in uselabels. \
                        if uselabels==None, all labels in input files are valid')

    args=parser.parse_args()
    edges_train, nodes_train, label_data_train, label_count_train=load_graph(args.train)
    edges_infer, nodes_infer, label_data_infer, label_count_infer=load_graph(args.infer)
    edges_other, nodes_other, _, _=load_graph(args.other)
    edges_all=edges_train | edges_infer | edges_other
    nodes_all=nodes_train | nodes_infer | nodes_other
    label_count_all = label_count_train.copy()
    label_count_all.update(label_count_infer)
    label_data_all={**label_data_train, **label_data_infer}
    print("#nodes:",len(nodes_all))
    print("#edge:",len(edges_all))
    print("#train and infer label:",len(label_data_all))
    label_dim=0
    label_use={}
    if (args.uselabels!=None):
        for i,el in enumerate(args.uselabels):
            label_use[el]=i
    else:
        for l,cnt in label_count_all.items():
            if cnt>args.num_label_thresh:
                i=len(label_use)
                label_use[l]=i
    label_dim=max(label_use.values())+1
    print("#label_dim:",label_dim)

    nodes_all=sorted(list(nodes_all))
    node_number={el:i for i,el in enumerate(nodes_all)}
    node_num=len(node_number)
    edge_types={"negative":0,"self":1}
    for _,e,_ in edges_all:
        if e not in edge_types:
            edge_types[e]=len(edge_types)
    ### constructing adj.                                                                             
    if (args.multiedge==True):
        adjs=[]
        graph_edges=[set() for _ in edge_types]
        for e in edges_all:
            t=edge_types[e[1]]
            graph_edges[t].add((node_number[e[0]],node_number[e[2]]))
            graph_edges[t].add((node_number[e[2]],node_number[e[0]]))
        for i in range(node_num):
            graph_edges[edge_types["self"]].add((i,i))
        for i,edge_set in enumerate(graph_edges):
            edge_list=sorted(list(edge_set))
            adj_idx=[]
            adj_val=[]
            for e in edge_list:
                adj_idx.append([e[0],e[1]])
                adj_val.append(1)
            if len(edge_list)>0:
                print(i,":",len(edge_list))
                adj=(np.array(adj_idx),np.array(adj_val),np.array((node_num,node_num)))
                adjs.append(adj)
        adjs=[adjs]
    else:
        graph_edges=set()
        for e in edges_all:
            graph_edges.add((node_number[e[0]],node_number[e[2]]))
            graph_edges.add((node_number[e[2]],node_number[e[0]]))
        for i in range(node_num):
            graph_edges.add((i,i))
        graph_edges=sorted(list(graph_edges))
        adj_idx=[]
        adj_val=[]
        for e in graph_edges:
            adj_idx.append([e[0],e[1]])
            adj_val.append(1)
        adjs=[(np.array(adj_idx),np.array(adj_val),np.array((node_num,node_num)))]

    node_label=[]
    mask_label=[]
    label_list_train=[]
    label_list_infer=[]
    for i,node_name in enumerate(nodes_all):
        if node_name in label_data_all.keys():
            label_original=label_data_all[node_name]
            if (label_original in label_use.keys()):
                label_converted=label_use[label_original]
                bit_on=np.zeros(label_dim,)
                bit_on[label_converted]=1
                node_label.append(bit_on)
                mask_label.append(1)
                if (node_name in label_data_train.keys()):
                    label_list_train.append([i, label_converted])
                else:
                    label_list_infer.append([i, label_converted])
            else:
                node_label.append([0]*label_dim)
                mask_label.append(0)
                if (node_name in label_data_train.keys()):
                    label_list_train.append([i, np.nan])
                else:
                    label_list_infer.append([i, np.nan])
        else:
            node_label.append([0]*label_dim)
            mask_label.append(0)
    print("#label_list_train:",len(label_list_train))
    print("#label_list_infer:",len(label_list_infer))

    obj={
        "adj":adjs,
        "node":np.array([list(range(node_num))]),
        "node_label":np.array([node_label]),
        "mask_node_label":np.array([mask_label]),
        "node_num":node_num,
        "label_list":np.array([label_list_train]),
        "test_label_list":np.array([label_list_infer]),
        "max_node_num":node_num}
    
    if (args.class_weight==True):
        # the dimension of class_weight should be the same as that of node_label/label_list_train/label_list_infer.
        # put 0 in class_weight where label is not in train set.
        class_weight=[0]*label_dim
        sum_cnt=0
        for key, cnt in label_count_train.items():
            if key in label_use.keys():
                m=label_use[key]
                class_weight[m]+=1.0/cnt
                print(f"#sample in class {key}  in train: {cnt}")
                sum_cnt+=1.0/cnt
        for m in range(label_dim):
            class_weight[m]/=sum_cnt
        print(f"label_use:{label_use}")
        print(f"class_weight={class_weight}")
        obj["class_weight"]=class_weight

    filename=args.output
    print("[SAVE]",filename)
    joblib.dump(obj, filename)

    nodes_filename=args.output_node
    print("[SAVE]",nodes_filename)
    fp=open(nodes_filename,"w")
    json.dump(nodes_all,fp)
