##
## python show_summary_result.py --output_node_info result/node_info.json
##

import json
import re
import numpy as np
import argparse 
import os

if __name__ == '__main__':
	##
	## コマンドラインのオプションの設定
	##
	parser = argparse.ArgumentParser(description = "Classification")
	parser.add_argument("--input_info",default="our.json",
		help = "result/cv_info.json", type = str)
	parser.add_argument('--model',default="rf",
		help = "", type=str)
	parser.add_argument('--output_dir',default="04data_",
		help = "output", type=str)
	args = parser.parse_args()
	np.random.seed(20) 
	
	## load
	filename=args.input_info
	print("[LOAD]",filename)
	ifp = open(filename, 'r')
	obj=json.load(ifp)
	## output directory
	out_dir=args.output_dir+args.model+"/"
	os.makedirs(out_dir,exist_ok=True)
	for filename,o in obj.items():
		test_y=[]
		prob_y=[]
		test_idx=[]
		for result in o["cv"]:
			test_idx.extend(result["test_idx"])
			test_y.extend(result["test_y"])
			prob_y.extend(result["prob_y"])
		data=[]
		for i,y,py in zip(test_idx,test_y,prob_y):
			data.append([i,y,py[1]])
		data=sorted(data)
		print("[LOAD]",filename)
		fp=open(filename)
		savefilename=out_dir+os.path.basename(filename)
		h=next(fp)
		head=h.split(",")
		print("[SAVE]",savefilename)
		ofp=open(savefilename,"w")
		ofp.write("LINE-ID,CHR,Nuc-Pos,REF-Nuc,ALT-Nuc,Label,"+args.model+"-SCORE\n")
		for d in data:
			line=next(fp)
			arr=line.split(",")
			name=arr[0]
			m=re.match(r'^(.+)_(\d+)_([ATGC])_([ATGC])$',name)
			if not m:
				print("[ERROR]", name)
			ofp.write(str(d[0]))
			ofp.write(",")
			ofp.write(",".join([m[1],m[2],m[3],m[4]]))
			ofp.write(",")
			ofp.write(str(d[1]))
			ofp.write(",")
			ofp.write(str(d[2]))
			ofp.write("\n")
			
	
