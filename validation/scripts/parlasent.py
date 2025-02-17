from pathlib import Path
import json
import re
import polars as pl

try:
    infile = snakemake.input[0]
    outfile = snakemake.output[0]
except NameError:
    infile = "data/input/1_coding_a_2010.csv"
    outfile = "data/parlasent/1_coding_a_2010.jsonl"


df = pl.read_csv(infile)
from simpletransformers.classification import ClassificationModel, ClassificationArgs
import torch

model_args = ClassificationArgs(
    regression=True,
)
model = ClassificationModel(
    model_type="xlmroberta",
    model_name="classla/xlm-r-parlasent",
    use_cuda=torch.cuda.is_available(),
    num_labels=1,
    args=model_args,
)
try:
    predictions, logits = model.predict(df["Text"].to_list())
except:
    predictions, logits = model.predict(df["sentence"].to_list())

df = df.with_columns(ParlaSent=predictions)

2 + 2
df.write_ndjson(outfile)
