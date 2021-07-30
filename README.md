# PathoGN : Pathogenicity prediction model with a graph neural network

## Example Usage
### Run the demo with Varibench datasets

> Varibench is a benchmark datasets for prediction of genomic variant effects.

Nair PS, Vihinen M. VariBench: A Benchmark Database for Variations. [_Hum Mutat_. 2013, 34(1):42-9](https://pubmed.ncbi.nlm.nih.gov/22903802/).

http://structure.bmc.lu.se/VariBench/

### 0. Install kGCN (https://github.com/clinfo/kGCN) with conda
```
$ conda create -n kgcn python=3.7 conda=4.9.2
$ conda activate kgcn
$ conda install tensorflow=1.15 joblib numpy scipy scikit-learn matplotlib pandas
$ pip install --upgrade git+https://github.com/clinfo/kGCN.git
```
* currently kGCN does NOT support TensorFlow 2

### 1. Get Valibench datasets
```
sh get_dataset.sh
```

### 2. Preprocessing data

```
sh build_dataset.sh
```

### 3. Get and preprocess Reactome data
```
sh make_reactome_data.sh
python script/preprocess_reactome.py 
```

### 4. make input data for GCN
```
sh make_data.sh
```

### 5. Run GCN and evaluate with cross validation
```
sh run_gcn.sh
```

### Prediction result
`score1-5.csv` will be created in `result`, and GCN-Score will be calculated for each of them.

The correspondence between numbers and data sets is as follows：
1. exovar_filtered_tool_scores
2. humvar_filtered_tool_scores
3. predictSNP_selected_tool_scores
4. swissvar_selected_tool_scores
5. varibench_selected_tool_scores


## The prediction scores for ClinVar 20200210 datasets

PathoGN predicted the pathogenicity for all variants that were not annotated as either pathogenic or benign in the 2020 ClinVar dataset.
The model was trained using the labeled data (pathogenic=10,877, benign=7504) and then used to make predictions for the 12,520 unlabeled variants.

The prediction result: `PredictionResults_ConflictVariant_ClinVar20200210.tsv`

These scores are also available on MGeND (https://mgend.med.kyoto-u.ac.jp/).

## Reference
```
@article {PathoGN,
        author = {Kamada, Mayumi and Takagi, Atsuko and Kojima, Ryosuke and Tanaka, Yoshihisa and Nakatsui, Masahiko and Tanabe, Noriko and Hirata, Makoto and Yoshida, Teruhiko and Okuno, Yasushi},
        title = {Network-based pathogenicity prediction for variants of uncertain significance},
        year = {2021},
        doi = {10.1101/2021.07.15.452566},
        eprint = {https://www.biorxiv.org/content/early/2021/07/16/2021.07.15.452566.full.pdf},
        journal = {bioRxiv}
}
```
