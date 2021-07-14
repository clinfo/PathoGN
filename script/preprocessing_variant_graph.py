import numpy as np
import csv
import os, sys
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
                    # single task
                    m=int(arr[1])
                    label_data[arr[0]]=m
                    if m not in label_count: label_count[m]=0
                    label_count[m]+=1
                    #dim=len(arr[1:])
                    #if label_dim<dim: label_dim=dim
                    nodes.add(arr[0])
    return edges, nodes, label_data, label_count
 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input',
        nargs='*',
        type=str)
    parser.add_argument('--multilabel', action='store_true')
    parser.add_argument('--relabel','-r', action='store_true')
    parser.add_argument('--class_weight','-w', action='store_true')
    parser.add_argument('--multiedge', action='store_true')
    parser.add_argument('--num_label_thresh','-n', type=int,
        default=0,
        help='data path')
    parser.add_argument('--output', type=str,
        default="sample_kg.jbl",
        nargs='?',
        help='save jbl file')
    parser.add_argument('--output_node', type=str,
        default="sample_kg_nodes.json",
        nargs='?',
        help='save json file')
    parser.add_argument('--mapping','-m', type=str,
        default=None,
        nargs='+',
        help='mapping')

    args=parser.parse_args()
    edges, nodes, label_data, label_count=load_graph(args.input)
    print("#nodes:",len(nodes))
    print("#edge:",len(edges))
    print("#label:",len(label_data))
    label_dim=0
    if args.relabel:
        if args.mapping:
            label_mapping={}
            for i,el in enumerate(args.mapping):
                for m in el.strip().split(","):
                    label_mapping[int(m)]=i
            label_dim=max(label_mapping.values())+1
            print("#label_dim:",label_dim)
        else:
            label_mapping={}
            for l,cnt in label_count.items():
                if cnt>args.num_label_thresh:
                    i=len(label_mapping)
                    label_mapping[l]=i
            label_dim=max(label_mapping.values())+1
            print("#label_dim:",label_dim)
    else:
        label_dim=max(label_data.values())+1
        print("#label_dim:",label_dim)

    #print("#label_dim:",label_dim)
    nodes=sorted(list(nodes))
    all_nodes={el:i for i,el in enumerate(nodes)}
    node_num=len(all_nodes)
    edge_types={"negative":0,"self":1}
    for _,e,_ in edges:
        if e not in edge_types:
            edge_types[e]=len(edge_types)
    print(edge_types)
    ### constructing adj.
    if args.multiedge:
        adjs=[]
        graph_edges=[set() for _ in edge_types]
        for e in edges:
            t=edge_types[e[1]]
            graph_edges[t].add((all_nodes[e[0]],all_nodes[e[2]]))
            graph_edges[t].add((all_nodes[e[2]],all_nodes[e[0]]))
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
        for e in edges:
            graph_edges.add((all_nodes[e[0]],all_nodes[e[2]]))
            graph_edges.add((all_nodes[e[2]],all_nodes[e[0]]))
        for i in range(node_num):
            graph_edges.add((i,i))
        graph_edges=sorted(list(graph_edges))
        adj_idx=[]
        adj_val=[]
        for e in graph_edges:
            adj_idx.append([e[0],e[1]])
            adj_val.append(1)
        adjs=[(np.array(adj_idx),np.array(adj_val),np.array((node_num,node_num)))]

    ###
    node_ids=np.array([list(range(node_num))])
    graph_names=["one"]
    max_node_num = node_num
    labels=[]
    mask_label=[]
    label_list=[]
    for i,el in enumerate(nodes):
        if el in label_data:
            if args.relabel:
                key=label_data[el]
                if key in label_mapping:
                    m=label_mapping[key]
                    vm=np.zeros((label_dim,))
                    vm[m]=1
                    labels.append(vm)
                    mask_label.append(1)
                    label_list.append([i,m])
                    #print(i,nodes[i])
                else:
                    labels.append([0]*label_dim)
                    mask_label.append(0)
            else:
                m=label_data[el]
                #vm = encoder.fit_transform([m]).toarray()
                vm=np.zeros((label_dim,))
                vm[m]=1
                labels.append(vm)
                mask_label.append(1)
                label_list.append([i,m])
        else:
            labels.append([0]*label_dim)
            mask_label.append(0)

    obj={
        "adj":adjs,
        "node":node_ids,
        "node_label":np.array([labels]),
        "mask_node_label":np.array([mask_label]),
        "node_num":max_node_num,
        "label_list":np.array([label_list]),
        "max_node_num":max_node_num}

    print("#label_list:",len(label_list))

    if args.class_weight:
        class_weight=[0]*label_dim
        sum_cnt=0
        for key, cnt in label_count.items():
            if args.relabel:
                if key in label_mapping:
                    m=label_mapping[key]
                    class_weight[m]+=1.0/cnt
                    print("class=",key," id=",m)
                    print("#sample:",cnt)
                    print("class wight:",class_weight[m])
                    sum_cnt+=1.0/cnt
                    #sum_cnt+=cnt
        for m in range(label_dim):
            class_weight[m]/=sum_cnt
        print(class_weight)
        obj["class_weight"]=class_weight
    filename=args.output
    print("[SAVE]",filename)
    joblib.dump(obj, filename)

    nodes_filename=args.output_node
    print("[SAVE]",nodes_filename)
    fp=open(nodes_filename,"w")
    json.dump(nodes,fp)


