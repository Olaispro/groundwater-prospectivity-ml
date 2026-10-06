"""Synthetic-only groundwater prospectivity workflow."""
import argparse,json
from pathlib import Path
def generate(n=600,seed=17):
 import numpy as np
 rng=np.random.default_rng(seed); lith=rng.integers(0,4,n); line=rng.uniform(0,1,n); drain=rng.uniform(0,1,n); slope=rng.uniform(0,1,n); rain=rng.normal(.5,.18,n).clip(0,1)
 score=.9*line-.6*drain-.5*slope+.7*rain+np.choose(lith,[.25,.1,-.15,-.05])+rng.normal(0,.2,n)
 return np.column_stack([lith,line,drain,slope,rain]),(score>np.quantile(score,.55)).astype(int)
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='results.json');p.add_argument('--seed',type=int,default=17);a=p.parse_args()
 from sklearn.model_selection import train_test_split
 from sklearn.ensemble import RandomForestClassifier
 from sklearn.metrics import accuracy_score,balanced_accuracy_score,confusion_matrix,roc_auc_score
 X,y=generate(seed=a.seed);Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=a.seed,stratify=y);m=RandomForestClassifier(n_estimators=150,min_samples_leaf=3,class_weight='balanced',random_state=a.seed);m.fit(Xtr,ytr);prob=m.predict_proba(Xte)[:,1];pred=(prob>=.5).astype(int)
 r={'dataset':'synthetic demonstration','seed':a.seed,'n':len(y),'test_n':len(yte),'accuracy':round(accuracy_score(yte,pred),3),'balanced_accuracy':round(balanced_accuracy_score(yte,pred),3),'roc_auc':round(roc_auc_score(yte,prob),3),'confusion_matrix':confusion_matrix(yte,pred).tolist(),'feature_importance':dict(zip(['lithology_code','lineament_density','drainage_density','slope','rainfall'],map(lambda x:round(float(x),3),m.feature_importances_))),'limitations':'Synthetic features and labels are illustrative only. No real wells, raster layers, spatial cross-validation, calibration, or field validation.'}
 Path(a.out).write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
