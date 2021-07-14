import os
import sys
import numpy as np


ignore_attrs=['True Label','CHR','Nuc-Pos','REF-Nuc','ALT-Nuc','Ensembl-Gene-ID','Uniprot-Accession']
#id_names=["Ensembl_geneid","Uniprot_id_Polyphen2"]
#id_names_prefix=["ENSMNL","Uniprot_id_Polyphen2"]
label_name="True Label"

def is_nan_symbol(el):
	return el=="" or el=="-" or el=="."

def make_key_id(head_mapping,arr):
	l=[arr[i] for i in [head_mapping["CHR"],head_mapping["Nuc-Pos"],head_mapping["REF-Nuc"],head_mapping["ALT-Nuc"]]]
	key_id="_".join(l)
	return key_id
	#

output_path="03data_table/"
os.makedirs(output_path,exist_ok=True)
for filename in sys.argv[1:]:
	score_data=[]
	#filename="dbnsfp_data/data_chr1.tsv"
	fp=open(filename)
	head=next(fp)
	head_arr=head.strip().split(",")

	header_mapping={el:i for i,el in enumerate(head_arr)}
	first=True
	enabled_head=[]
	for line in fp:
		arr=line.strip().split(",")
		#for index
		key_id=make_key_id(header_mapping,arr)
		data_line=[]
		data_line.append(key_id)
		if first: enabled_head.append("key")
		
		#for label
		label_index=header_mapping[label_name]
		label_el=arr[label_index]
		label_arr=set(label_el.split("|"))
		if len(label_arr)==1:
			el=list(label_arr)[0]
			data_line.append(el)
			if first: enabled_head.append(label_name)
		else:
			continue
		#for score data
		for i,el in enumerate(arr):
			k=head_arr[i]
			if not k in ignore_attrs:
				if not is_nan_symbol(el):
					data_line.append(el)
					if first: enabled_head.append(k)
				else:
					data_line.append("")
					if first: enabled_head.append(k)
		score_data.append(data_line)
		first=False
		
	basename=os.path.basename(filename)
	out_fp=open(output_path+basename,"w")
	s=",".join(enabled_head)
	out_fp.write(s)
	out_fp.write("\n")
	for pair in score_data:
		s=",".join(pair)
		out_fp.write(s)
		out_fp.write("\n")

