#!/bin/sh
cd `dirname $0`
mkdir -p dataset
mkdir -p config

mv 03data_graph/reactome.graph.tsv 03data_graph/reactome.graph.old

python script/make_config.py

#
python script/preprocessing_variant_graph.py \
  ./03data_graph/exovar_filtered_tool_scores/*.tsv ./03data_graph/*.tsv \
  --relabel --mapping -1 1 -w --output dataset/dataset1.jbl --output_node dataset/dataset_nodes1.json
python script/preprocessing_variant_graph.py \
  ./03data_graph/humvar_filtered_tool_scores/*.tsv ./03data_graph/*.tsv \
  --relabel --mapping -1 1 -w --output dataset/dataset2.jbl --output_node dataset/dataset_nodes2.json
python script/preprocessing_variant_graph.py \
  ./03data_graph/predictSNP_selected_tool_scores/*.tsv ./03data_graph/*.tsv \
  --relabel --mapping -1 1 -w --output dataset/dataset3.jbl --output_node dataset/dataset_nodes3.json
python script/preprocessing_variant_graph.py \
  ./03data_graph/swissvar_selected_tool_scores/*.tsv ./03data_graph/*.tsv \
  --relabel --mapping -1 1 -w --output dataset/dataset4.jbl --output_node dataset/dataset_nodes4.json
python script/preprocessing_variant_graph.py \
  ./03data_graph/varibench_selected_tool_scores/*.tsv ./03data_graph/*.tsv \
  --relabel --mapping -1 1 -w --output dataset/dataset5.jbl --output_node dataset/dataset_nodes5.json

python script/preprocessing_variant_graph.py --multiedge\
  ./03data_graph/exovar_filtered_tool_scores/*.tsv ./03data_graph/*.tsv \
  --relabel --mapping -1 1 -w --output dataset/dataset1m.jbl --output_node dataset/dataset_nodes1m.json
python script/preprocessing_variant_graph.py  --multiedge\
  ./03data_graph/humvar_filtered_tool_scores/*.tsv ./03data_graph/*.tsv\
  --relabel --mapping -1 1 -w --output dataset/dataset2m.jbl --output_node dataset/dataset_nodes2m.json
python script/preprocessing_variant_graph.py  --multiedge\
  ./03data_graph/predictSNP_selected_tool_scores/*.tsv ./03data_graph/*.tsv \
  --relabel --mapping -1 1 -w --output dataset/dataset3m.jbl --output_node dataset/dataset_nodes3m.json
python script/preprocessing_variant_graph.py  --multiedge\
  ./03data_graph/swissvar_selected_tool_scores/*.tsv ./03data_graph/*.tsv \
  --relabel --mapping -1 1 -w --output dataset/dataset4m.jbl --output_node dataset/dataset_nodes4m.json
python script/preprocessing_variant_graph.py  --multiedge\
  ./03data_graph/varibench_selected_tool_scores/*.tsv ./03data_graph/*.tsv \
  --relabel --mapping -1 1 -w --output dataset/dataset5m.jbl --output_node dataset/dataset_nodes5m.json



