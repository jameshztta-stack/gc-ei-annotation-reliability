#!/usr/bin/env python3
"""Pinned retrospective confidence comparison. NEVER fresh test or risk certification."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, brier_score_loss

CHECKSUMS = {
 "609": "62899a9be61118299e730558fe097e61e7423411d6ea33ea678245f282b41dd7",
 "1410": "67a209e835279852a91e92abad7a3598fd38f6fd6978082b75c46d6eb4a745ce",
 "466": "09a228acbf93fb307b9150ff47024c253e4e94ea4223f8cc309fc8083afdc11b",
}
def read(path, role):
 p=Path(path)
 if hashlib.sha256(p.read_bytes()).hexdigest()!=CHECKSUMS[role]:
  raise RuntimeError("Original archival file checksum mismatch: "+role)
 d=pd.read_csv(p)
 if len(d)!=int(role): raise RuntimeError("Unexpected denominator: "+role)
 return d

def compare(d,yname,features):
 y=d[yname].to_numpy(dtype=int)
 if set(y)!={0,1}:raise RuntimeError("Both classes required")
 v={"n":len(y),"correct":int(y.sum())}
 for name,col in features.items():
  s=d[col].to_numpy(dtype=float)
  if not np.isfinite(s).all():raise RuntimeError("Nonfinite feature "+name)
  x={"AUROC":float(roc_auc_score(y,s))}
  if name.startswith("HGB") or name.startswith("logit"):
   if (s<0).any() or (s>1).any():raise RuntimeError("Not model probability")
   x["Brier"]=float(brier_score_loss(y,s))
  v[name]=x
 return v

def risk_curve(d,yname,features):
 y=d[yname].to_numpy(dtype=int)
 result=pd.DataFrame({"accepted_n":np.arange(1,len(d)+1)})
 result["coverage"]=result.accepted_n/len(d)
 for key,col in features.items():
  s=d[col].to_numpy(dtype=float)
  ordered=np.argsort(-s,kind="stable")
  wrong=np.cumsum(1-y[ordered])
  result[key+"_wrong_n"]=wrong
  result[key+"_error_rate"]=wrong/result.accepted_n
 return result

def reliability(d,yname,col):
 y=d[yname].to_numpy(dtype=int);p=d[col].to_numpy(dtype=float)
 out=[]
 for k in range(10):
  low=k/10;hi=(k+1)/10
  mask=(p>=low)&((p<hi) if k<9 else (p<=1.0))
  n=int(mask.sum())
  out.append({"bin_low":low,"bin_high":hi,"n":n,"correct":int(y[mask].sum()),
   "mean_probability":float(p[mask].mean()) if n else None,
   "correct_fraction":float(y[mask].mean()) if n else None})
 bins=pd.DataFrame(out)
 ece=sum(row.n*abs(row.mean_probability-row.correct_fraction)
         for row in bins.itertuples() if row.n)/len(d)
 return bins,float(ece)


def make_figures(out, a, c, evaluations):
 """Publication-ready source-label DESCRIPTIVE plots; not independent validation."""
 import matplotlib
 matplotlib.use("Agg")
 import matplotlib.pyplot as plt
 # All signals rank THE SAME frozen m1 top-one candidate for correctness.
 fig,ax=plt.subplots(figsize=(7,4.3))
 names=["Top cosine","Top-two margin","Frozen HGB"]
 values=[evaluations["609"][k]["AUROC"] for k in ("similarity","margin","HGB")]
 bars=ax.bar(names,values)
 ax.set_ylim(0,1)
 ax.set_ylabel("AUROC for publisher first14 top-1 agreement")
 ax.set_title("609 previously evaluated within-source EI cases")
 for bar,value in zip(bars,values):
  ax.text(bar.get_x()+bar.get_width()/2,value+.015,f"{value:.3f}",ha="center")
 fig.tight_layout()
 fig.savefig(out/"Figure_1_609_AUROC_baselines.png",dpi=200)
 plt.close(fig)

 for frame,role,ycol,pcol in [(a,"609","m1_top1_correct","HGB_probability"),
                              (c,"466","m1_top1_correct","HGB_probability_devfit")]:
  bins,_=reliability(frame,ycol,pcol)
  keep=bins.loc[bins.n>0]
  fig,ax=plt.subplots(figsize=(6,5.6))
  ax.plot([0,1],[0,1],linestyle="--",label="Perfect agreement")
  ax.plot(keep.mean_probability,keep.correct_fraction,"o-",label="Observed bin fraction")
  for row in keep.itertuples():
   ax.annotate("n="+str(row.n),(row.mean_probability,row.correct_fraction),
               textcoords="offset points",xytext=(5,8),fontsize=8)
  ax.set(xlim=(0,1),ylim=(0,1),
         xlabel="Mean HGB score per fixed-width bin",
         ylabel="Source first14 correctness fraction",
         title=role+" retrospective source-labelled cases")
  ax.legend()
  fig.tight_layout()
  fig.savefig(out/("Figure_2_"+role+"_HGB_reliability.png"),dpi=200)
  plt.close(fig)

  cr=risk_curve(frame,ycol,{"HGB":pcol,
       "margin":"feature_top1_minus_top2" if role=="609" else "m1_top1_minus_top2",
       "similarity":"m1_top1_cosine"})
  fig,ax=plt.subplots(figsize=(7,5))
  for label in ("HGB","margin","similarity"):
   ax.plot(cr.coverage*100,cr[label+"_error_rate"]*100,label=label)
  ax.set(xlim=(0,100),ylim=(0,100),
         xlabel="Accepted fraction of archived observations (%)",
         ylabel="Observed errors / accepted observations (%)",
         title=role+" matched-coverage retrospective risk curves")
  ax.legend(title="Fixed ranking signal")
  fig.tight_layout()
  fig.savefig(out/("Figure_3_"+role+"_acceptance_error.png"),dpi=200)
  plt.close(fig)

def main():
 ap=argparse.ArgumentParser()
 for x in ("609","1410","466"):ap.add_argument("--input-"+x,required=True)
 ap.add_argument("--out",default="phase3_recomputed")
 z=ap.parse_args();out=Path(z.out);out.mkdir(parents=True,exist_ok=True)
 a=read(getattr(z,"input_609"),"609")
 b=read(getattr(z,"input_1410"),"1410")
 c=read(getattr(z,"input_466"),"466")
 assert a.source_database_first14_label.nunique()==609
 assert c.true_publisher_first14.nunique()==419
 assert (a.m1_top1_correct.sum(),b.top1_correct_source_database_label.sum(),c.m1_top1_correct.sum())==(394,901,334)
 assert (a.accept_10pct.sum(),a.accept_5pct.sum())==(198,38)
 assert int(((a.accept_10pct==1)&(a.m1_top1_correct==0)).sum())==12
 assert int(((a.accept_5pct==1)&(a.m1_top1_correct==0)).sum())==0
 A={"HGB":"HGB_probability","margin":"feature_top1_minus_top2","similarity":"m1_top1_cosine"}
 B={"HGB":"oof_expanded_12f_HGB","logit12":"oof_expanded_12f_logit",
    "logit5":"oof_baseline_5f_logit","margin":"feature_top1_minus_top2","similarity":"feature_top_score"}
 C={"HGB":"HGB_probability_devfit","margin":"m1_top1_minus_top2","similarity":"m1_top1_cosine"}
 evaluations={
  "609":compare(a,"m1_top1_correct",A),
  "1410":compare(b,"top1_correct_source_database_label",B),
  "466":compare(c,"m1_top1_correct",C)}
 for role,frame,label,features in [("609",a,"m1_top1_correct",A),("466",c,"m1_top1_correct",C)]:
  risk=risk_curve(frame,label,features)
  risk.to_csv(out/("risk_"+role+".csv"),index=False)
  rel,ece=reliability(frame,label,features["HGB"])
  rel.to_csv(out/("reliability_"+role+".csv"),index=False)
  evaluations[role]["ECE10"]=ece
  levels=[38,198,305,457,609] if role=="609" else [25,185,233,349,466]
  evaluations[role]["matched_acceptance_wrong_counts"]={
   str(k):{name:int(risk.iloc[k-1][name+"_wrong_n"]) for name in features} for k in levels}
 assert abs(evaluations["609"]["HGB"]["AUROC"]-0.8633042143784677)<1e-12
 assert abs(evaluations["609"]["HGB"]["Brier"]-0.1406447500413923)<1e-12
 assert abs(evaluations["466"]["HGB"]["AUROC"]-0.8700893667211033)<1e-12
 assert abs(evaluations["1410"]["HGB"]["AUROC"]-0.8552764991528732)<1e-12
 assert evaluations["609"]["matched_acceptance_wrong_counts"]["198"]=={"HGB":12,"margin":11,"similarity":45}
 assert evaluations["609"]["matched_acceptance_wrong_counts"]["38"]=={"HGB":0,"margin":1,"similarity":10}
 evaluations["scope"]="RETROSPECTIVE; original 609 spent; first14 source-label agreement; no formal risk guarantee"
 make_figures(out,a,c,evaluations)
 evaluations["SHA256"]=CHECKSUMS
 (out/"summary.json").write_text(json.dumps(evaluations,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({role:evaluations[role] for role in ("609","1410","466")},indent=2))
if __name__=="__main__":main()
