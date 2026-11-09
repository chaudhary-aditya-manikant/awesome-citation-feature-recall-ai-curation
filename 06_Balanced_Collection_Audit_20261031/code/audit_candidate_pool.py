#!/usr/bin/env python3
"""Recompute core metadata checks for an OpenAlex candidate-pool CSV."""
import argparse, json
from pathlib import Path
import pandas as pd

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    df=pd.read_csv(args.input)
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    summary={
      'records':int(len(df)), 'unique_openalex_ids':int(df.openalex_id.nunique()),
      'missing_title':int(df.title.isna().sum()), 'missing_doi':int(df.doi.isna().sum()),
      'missing_abstract':int(df.abstract.isna().sum()), 'retracted_true':int(df.is_retracted.fillna(False).sum()),
      'zero_citations':int(df.citations.eq(0).sum()), 'citation_median':float(df.citations.median()),
      'year_counts':{str(int(k)):int(v) for k,v in df.year.value_counts().sort_index().items()},
      'language_counts':{str(k):int(v) for k,v in df.metadata_language.value_counts(dropna=False).items()},
      'type_counts':{str(k):int(v) for k,v in df.type.value_counts(dropna=False).items()}
    }
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    df.type.value_counts().rename_axis('type').reset_index(name='records').to_csv(out/'type_counts.csv',index=False)
    df.metadata_language.value_counts(dropna=False).rename_axis('metadata_language').reset_index(name='records').to_csv(out/'language_counts.csv',index=False)
    df.year.value_counts().sort_index().rename_axis('year').reset_index(name='records').to_csv(out/'year_counts.csv',index=False)
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
