import os
import sys
import numpy as np

ignore_attrs=['True Label','CHR','Nuc-Pos','REF-Nuc','ALT-Nuc','Ensembl-Gene-ID','Uniprot-Accession']
label_name="True Label"

#id_names=["Ensembl_geneid","Uniprot_id_Polyphen2"]
#id_names_prefix=["ENSMNL","Uniprot_id_Polyphen2"]

def is_nan_symbol(el):
	return el=="" or el=="-" or el=="."


def make_key_id(head_mapping,arr):
	l=[arr[i] for i in [head_mapping["CHR"],head_mapping["Nuc-Pos"],head_mapping["REF-Nuc"],head_mapping["ALT-Nuc"]]]
	key_id="_".join(l)
	return key_id
	
for filename in sys.argv[1:]:
	id_data=[]
	score_data=[]
	label_data=[]
	#filename="dbnsfp_data/data_chr1.tsv"
	fp=open(filename)
	head=next(fp)
	head_arr=head.strip().split(",")

	header_mapping={el:i for i,el in enumerate(head_arr)}
	
	for line in fp:
		arr=line.strip().split(",")
		#for index
		key_id=make_key_id(header_mapping,arr)
		#for data: "Ensembl_geneid"
		id_name='Ensembl-Gene-ID'
		id_index=header_mapping[id_name]
		id_el=arr[id_index]
		for el in id_el.split(";"):
			if el!=".":
				id_data.append([key_id,"ENSEMBL:"+el])
		
		#for data: "Uniprot_id_Polyphen2"
		id_name='Uniprot-Accession'
		id_index=header_mapping[id_name]
		id_el=arr[id_index]
		for el in id_el.split(";"):
			if el!=".":
				id_data.append([key_id,el])
		#for score data
		for i,el in enumerate(arr):
			k=head_arr[i]
			if not k in ignore_attrs and not is_nan_symbol(el):
				#score_data.append([key_id,el])
				score_data.append([key_id,k+":"+el])
		#for label
		label_index=header_mapping[label_name]
		label_el=arr[label_index]
		label_arr=set(label_el.split("|"))
		if len(label_arr)==1:
			el=list(label_arr)[0]
			label_data.append([key_id,el])
	name, _ = os.path.splitext(os.path.basename(filename))
	output_path="03data_graph/"+name+"/"
	os.makedirs(output_path,exist_ok=True)
	print(len(score_data))
	out_fp=open(output_path+"feature.graph.tsv","w")
	for pair in score_data:
		s="\t".join(pair)
		out_fp.write(s)
		out_fp.write("\n")

	print(len(id_data))
	out_fp=open(output_path+"id.graph.tsv","w")
	for pair in id_data:
		s="\t".join(pair)
		out_fp.write(s)
		out_fp.write("\n")

	print(len(label_data))
	out_fp=open(output_path+"var.label.tsv","w")
	for pair in label_data:
		s="\t".join(pair)
		out_fp.write(s)
		out_fp.write("\n")

