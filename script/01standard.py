import os
import sys
import numpy as np
ignore_attrs=['True Label','#RS-ID','CHR','Nuc-Pos','REF-Nuc','ALT-Nuc','Ensembl-Gene-ID','Ensembl-Protein-ID','Ensembl-Transcript-ID','Uniprot-Accession']
os.makedirs("01data_standard",exist_ok=True)
for filename in sys.argv[1:]:
	#filename="dbnsfp_data/data_chr1.tsv"
	fp=open(filename)
	head=next(fp)
	head_arr=head.strip().split(",")

	header_mapping={el:i for i,el in enumerate(head_arr)}
	data=[[] for _ in head_arr]
	for line in fp:
		arr=line.strip().split(",")
		for i,el in enumerate(arr):
			data[i].append(el)
	print("#attrs:",len(data))
	for i,d in enumerate(data):
		flag=False
		for el in d:
			if ";" in el:
				flag=True
		if flag:
			print(head_arr[i])
	for a in header_mapping.keys():
		if a not in ignore_attrs:
			index=header_mapping[a]
			for i,el in enumerate(data[index]):
				e_arr=[]
				arr=el.split(";")
				for x in arr:
					if x!= "" and x!="." and x!="-": e_arr.append(x)
				if len(e_arr)>=2:
					x=np.mean(list(map(float,e_arr)))
					
					data[index][i]=x
				elif len(e_arr)==1:
					data[index][i]=e_arr[0]
				else:
					data[index][i]="."
			#attr=header_mapping["SIFT_score"]
	output=list(map(list, zip(*data)))
	basename=os.path.basename(filename)
	out_filename="01data_standard/"+basename
	print("[SAVE]",out_filename)
	fp=open(out_filename,"w")
	fp.write(head)
	for arr in output:
		fp.write(",".join(map(str,arr)))
		fp.write("\n")

