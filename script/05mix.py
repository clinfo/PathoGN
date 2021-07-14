import json
import re
import numpy as np
import argparse 
import os

if __name__ == '__main__':
	##
	## コマンドラインのオプションの設定
	##
	parser = argparse.ArgumentParser(description = "classification")
	parser.add_argument("--input",default=[],
		help = "input files", type = str,nargs='+')
	parser.add_argument('--output',default=None,
		help = "output", type=str)
	args = parser.parse_args()
	np.random.seed(20) 
	
	## load
	data={}
	data_pos={}
	score_names=[]
	for filename in args.input:
		print("[LOAD]",filename)
		fp=open(filename)
		line=next(fp)
		arr=line.strip().split(",")
		score_names.append(arr[6])
		for line in fp:
			#LINE-ID,CHR,Nuc-Pos,REF-Nuc,ALT-Nuc,Label,svm-SCORE
			arr=line.strip().split(",")
			key="_".join(arr[1:5])
			if key not in data:
				data[key]=[]		
				data_pos[key]=arr[0:6]
			data[key].append(arr[6])
	if args.output is not None:
		filename=args.output
		print("[SAVE]",filename)
		fp=open(filename,"w")
		fp.write("ID,CHR,Nuc-Pos,REF-Nuc,ALT-Nuc,Label,"+",".join(score_names)+"\n")
		for k,v in data.items():
			if len(v)!=len(args.input):
				print("[ERROR]",k)
			fp.write(",".join(data_pos[k]))
			fp.write(",")
			fp.write(",".join(v))
			fp.write("\n")
