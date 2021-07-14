#!/usr/bin python
#-*- coding:utf-8 -*-
import os
import sys
import argparse

import collections
import numpy as np
def download(url,filename):
    print("... downloading:",url)
    urllib.request.urlretrieve(url,filename)
    print("[SAVE]",filename)
    
#filename=check_and_download_hint()
filename="reactome/reactome.homo_sapiens.interactions.tab-delimited.txt"
fp=open(filename)
head=next(fp)
head_arr=head.strip().split("\t")

head_mapping={k:i for i,k in enumerate(head_arr)}

#["# Interactor 1 uniprot id","Interactor 1 Ensembl gene id","Interactor 1 Entrez Gene id","Interactor 2 uniprot id","Interactor 2 Ensembl gene id","Interactor 2 Entrez Gene id","Interaction type","Interaction context","Pubmed references"]
outfilename="data/reactome.graph.tsv"
outfp=open(outfilename,"w")
count=0
for line in fp:
    arr=line.strip().split("\t")
    id1=head_mapping["Interactor 1 Ensembl gene id"]
    el1=arr[id1]
    if el1=="-":
        id1=head_mapping["# Interactor 1 uniprot id"]    
        el1=arr[id1]
    id2=head_mapping["Interactor 2 Ensembl gene id"]
    el2=arr[id2]
    if el2=="-":
        id2=head_mapping["Interactor 2 uniprot id"]    
        el2=arr[id2]
    if el1=="-" or el2=="-":
        print("[skip]")
        continue
    id3=head_mapping["Interaction type"]
    el3=arr[id3]
    outfp.write("\t".join([el1,el3,el2]))    
    count+=1
    outfp.write("\n")
print(count)

