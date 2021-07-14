import sys
import os


if len(sys.argv)>1:
	filenames=sys.argv[1:]
os.makedirs("00data",exist_ok=True)
for filename in filenames:
	header=None
	basename=os.path.basename(filename)
	out_filename="00data/"+basename
	print("[SAVE]",out_filename)
	fp=open("00data/"+basename,"w")
	for i,l in enumerate(open(filename)):
		header_line=False
		arr=l.strip().split(",")
		if i==0:
			header_line=True
			header=arr
		index_label=[header.index('True Label')]
		index_id=[]
		index_id.append(header.index('CHR'))
		index_id.append(header.index('Nuc-Pos'))
		index_id.append(header.index('REF-Nuc'))
		index_id.append(header.index('ALT-Nuc'))
		
		index_key=[]
		index_key.append(header.index('Ensembl-Gene-ID'))
		index_key.append(header.index('Uniprot-Accession'))
		
		index_feature=[]
		#index_feature.append(header.index('MAF'))
		index_feature.append(header.index('MutationTaster'))
		index_feature.append(header.index('MutationAssessor'))
		index_feature.append(header.index('PolyPhen2'))
		index_feature.append(header.index('CADD'))
		index_feature.append(header.index('SIFT'))
		index_feature.append(header.index('LRT'))
		index_feature.append(header.index('FatHMM-U'))
		index_feature.append(header.index('FatHMM-W'))
		index_feature.append(header.index('GERP++'))
		index_feature.append(header.index('PhyloP'))


		label=[arr[idx] for idx in index_label]
		ids=[arr[idx] for idx in index_id]
		key=[arr[idx] for idx in index_key]
		feature=[arr[idx] for idx in index_feature]
		
		out=label+ids+key+feature
		if not header_line:
			out=[el if el!="nan" else "." for el in out]
		fp.write(",".join(out))
		fp.write("\n")

