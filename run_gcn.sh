#!/bin/sh
cd `dirname $0`
mkdir -p result_gcn
mkdir -p log

#kgcn train_cv --config config/config.1.json  --cpu > ./sample_kg/varibench/log1.txt 2>&1 &
for i in `seq 1 5`
do
# kgcn train_cv --config config/config.${i}_gcn.json  --cpu > log/log${i}_gcn.txt 2>&1 &
kgcn train_cv --config config/config.${i}_gcn.json  > log/log${i}_gcn.txt 2>&1 &
done

wait

python script/show_summary_result.py \
  --output_node_info result_gcn/node_info.json \
  --input result_gcn/cv_info*.json \
  --output_csv result_gcn/summary.csv

#python show_node_info.py --input result_gcn/node_info.json --input_node ./sample_kg_nodes1.json --key result_gcn/cv_info1.json --output_csv result_gcn/score1.csv

for i in `seq 1 5`
do
python script/show_node_info.py \
  --input       result_gcn/node_info.json \
  --input_node  dataset/dataset_nodes${i}.json \
  --key         result_gcn/cv_info${i}.json \
  --output_csv  result_gcn/score${i}.csv
done

