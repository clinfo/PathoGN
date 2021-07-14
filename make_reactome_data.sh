mkdir -p reactome
wget https://reactome.org/download/current/interactors/reactome.homo_sapiens.interactions.tab-delimited.txt -O reactome/reactome.homo_sapiens.interactions.tab-delimited.txt

python script/make_reactome_graph.py

