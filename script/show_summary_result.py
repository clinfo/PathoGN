##
## python show_summary_result.py --output_node_info result/node_info.json
##

import json
import sklearn
import sklearn.metrics
import numpy as np
import argparse 

class NumPyArangeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist() # or map(int, obj)
        return json.JSONEncoder.default(self, obj)


def run(args):
    all_result={}
    all_node_info={}
    for filename in args.input:
        print(filename)
        ifp = open(filename, 'r')
        obj=json.load(ifp)
        results=[]
        node_info=[]
        for j in range(len(obj)):
            result={}
            pred_all_y=np.array(obj[j]['prediction_data'][0])
            label_index=obj[j]['test_labels'][0]
            ##
            ##
            prob_y=[]
            test_y=[]
            for index,l in label_index:
                py=pred_all_y[index]
                prob_y.append(py)
                test_y.append(l)
                node_info.append([index,l,py])
            prob_y=np.array(prob_y)
            test_y=np.array(test_y)
            pred_y=np.argmax(prob_y,axis=1)
            result["test_y"]=test_y
            result["pred_y"]=pred_y
            ###
            auc = sklearn.metrics.roc_auc_score(test_y,prob_y[:,1],average='macro')
            roc_curve = sklearn.metrics.roc_curve(test_y,prob_y[:,1],pos_label=1)
            result["roc_curve"]=roc_curve
            result["auc"]=auc
            precision, recall, f1, support=sklearn.metrics.precision_recall_fscore_support(test_y,pred_y)
            result["precision"]=precision
            result["recall"]=precision
            result["f1"]=f1
            conf=sklearn.metrics.confusion_matrix(test_y, pred_y)
            result["confusion"]=conf
            accuracy = sklearn.metrics.accuracy_score(test_y,pred_y)
            result["accuracy"]=accuracy
            #print(obj[j]['prediction_data'])
            #print(obj[j]['test_labels'])
            #print(obj[j]['test_data_idx'])

            #print(obj[j]['training_acc'])
            #print(obj[j]['validation_acc'])
            #print(obj[j]['training_cost'])
            #print(obj[j]['validation_cost'])
            results.append(result)
        ##
        ## cross-validation の結果をまとめる
        ## ・各評価値の平均・標準偏差を計算する
        ##
        cv_result={"cv": results}
        print("=================================")
        print("== Evaluation ... ")
        print("=================================")
        if args.task=="regression":
            score_names=["r2","mse"]
        else:
            score_names=["accuracy","f1","precision","recall","auc"]
        for score_name in score_names:
            scores=[r[score_name] for r in results]
            test_mean = np.nanmean(np.asarray(scores))
            test_std = np.nanstd(np.asarray(scores))
            print("Mean %10s on test set: %3f (standard deviation: %3s)"
                % (score_name,test_mean,test_std))
            cv_result[score_name+"_mean"]=test_mean
            cv_result[score_name+"_std"]=test_std
        ##
        ## 全体の評価
        ##
        test_y=[]
        pred_y=[]
        for result in cv_result["cv"]:
            test_y.extend(result["test_y"])
            pred_y.extend(result["pred_y"])
        if args.task!= "regression":
            conf=sklearn.metrics.confusion_matrix(test_y, pred_y)
            cv_result["confusion"]=conf
        cv_result["task"]=args.task
        ##
        ## 結果をディクショナリに保存して返値とする
        ##
        all_result[filename]=cv_result
        all_node_info[filename]=node_info
    return all_result,all_node_info

if __name__ == '__main__':
    ##
    ## コマンドラインのオプションの設定
    ##
    parser = argparse.ArgumentParser(description = "Classification")
    parser.add_argument("--input",default=["result/cv_info1.json"],
        help = "result/cv_info.json", type = str,nargs='+')
    parser.add_argument("--task",default="auto",
        help = "task type (auto/binary/multiclass/regression)", type = str)
    parser.add_argument('--output_json',default=None,
        help = "output: json", type=str)
    parser.add_argument('--output_csv',default=None,
        help = "output: csv", type=str)
    parser.add_argument('--output_node_info',default=None,
        help = "output: json", type=str)
    args = parser.parse_args()
    np.random.seed(20)

    all_result,all_node_info=run(args)
    ##
    ## 結果を簡易に表示
    ##
    if args.task=="regression":
        score_names=["r2","mse"]
    else:
        score_names=["accuracy","auc"]
    print("=================================")
    print("== summary ... ")
    print("=================================")
    metrics_names=sorted([m+"_mean" for m in score_names]+[m+"_std" for m in score_names])
    print("\t".join(["filename"]+metrics_names))
    for key,o in all_result.items():
        arr=[key]
        for name in metrics_names:
            arr.append("%2.4f"%(o[name],))
        print("\t".join(arr))

    ##
    ## 結果をjson ファイルに保存
    ## 予測結果やcross-validationなどの細かい結果も保存される
    ##
    if args.output_json:
        print("[SAVE]",args.output_json)
        fp = open(args.output_json, "w")
        json.dump(all_result,fp, indent=4, cls=NumPyArangeEncoder)

    ##
    ## 結果をcsv ファイルに保存
    ##
    if args.output_csv:
        print("[SAVE]",args.output_csv)
        fp = open(args.output_csv, "w")
        if args.task=="regression":
            score_names= ["r2","mse"]
        else:
            score_names= ["accuracy","f1","precision","recall","auc"]
        metrics_names=sorted([m+"_mean" for m in score_names]+[m+"_std" for m in score_names])
        fp.write("\t".join(["filename"]+metrics_names))
        fp.write("\n")
        for key,o in all_result.items():
            arr=[key]
            for name in metrics_names:
                arr.append("%2.4f"%(o[name],))
            fp.write("\t".join(arr))
            fp.write("\n")

    if args.output_node_info:
        print("[SAVE]",args.output_node_info)
        fp = open(args.output_node_info, "w")
        json.dump(all_node_info,fp, indent=4, cls=NumPyArangeEncoder)
