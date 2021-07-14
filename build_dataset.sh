python script/00get_features.py ./data/*.csv
python script/01standard.py ./00data/*.csv
python script/02desc.py ./01data_standard/*.csv
python script/03tograph.py 02data_desc_val/*.csv
#python script/03totable.py 02data_desc_val/*.csv
python script/03totable.py 01data_standard/*.csv
