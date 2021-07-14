import json

def generate(j,method,data_id,model):
    print("[LOAD] config.pathoGN.varibench.json")
    ifp = open("config.pathoGN.varibench.json", 'r')
    obj=json.load(ifp)
    for k,v in obj.items():
        if type(v) is str and ("<id>" in v or "<method>" in v or "<data>" in v or "model" in v):
            obj[k]=v.replace("<id>",j).replace("<method>",method).replace("<data>",data_id).replace("<model>",model)
    print("[SAVE]","config/config."+j+method+".json")
    fp = open("config/config."+j+method+".json", 'w')
    json.dump(obj,fp)

for i in range(5):
    j=str(i+1)
    generate(j,"_gcn",j,"model_gcn:GCN")
    #generate(j,"_mgcn",j+"m","model_gcn:GCN")
    #generate(j,"_gin",j,"model_gin:GIN")
    #generate(j,"_mgin",j+"m","model_gin:GIN")

