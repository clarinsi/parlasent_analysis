from pathlib import Path

try:
    infile = snakemake.input.parlasent_de
    outpng = snakemake.output.png
    outjson = snakemake.output.json
    chatgpt = snakemake.input.gpt
    dataset = snakemake.params.name
except:
    chatgpt = "data/german_with_GPT_preds.jsonl"
    infile = "data/parlasent/bundestag_raw_and_counts_DE.jsonl"
    outpng = "brisi.png"
    outjson = "brisi.json"
    dataset = "German validation dataset"

import polars as pl
import numpy as np

first = pl.read_csv("data/de_dict/DE_bundestag/bundestag_raw_and_counts_DE.csv")
second = pl.read_csv("data/de_dict/DE_bundestag/bundestag_sentiment_coding_DE.csv")
third = pl.read_ndjson(infile).select(["ParlaSent", "Qnum"])
gpt = pl.read_ndjson(chatgpt).select(["text", "GPT_pred"])
df = (
    first.join(second, on="Qnum").join(third, on="Qnum")
    # .with_columns(key=pl.col("sentence").str.strip_chars().str.to_lowercase())
).insert_column(-1, gpt["GPT_pred"])

# Uniform dataframes:
df = df.rename(
    {
        "vote": "gold",
        "GPT_pred": "GPT",
        "sentiment.norm": "dictionary score",
        # ""
    },
    strict=False,
)
print(df)
df.write_ndjson(outjson)
2 + 2
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

mapper = {
    "Clearly negative": 0,
    "Rather negative": 1,
    "Neutral": 2,
    "Rather positive": 3,
    "Clearly positive": 4,
}
df = df.with_columns(
    pl.col("gold").map_elements(lambda s: mapper.get(s, 99), return_dtype=pl.UInt8)
)


def corrfunc(x, y, hue=None, ax=None, **kws):
    """Plot the correlation coefficient in the top left hand corner of a plot."""
    r, p = spearmanr(x, y)

    ax = ax or plt.gca()
    ax.annotate(rf"$\rho$ = {r:.3f}, {p=:.1e}", xy=(0.1, 0.05), xycoords=ax.transAxes)


df_pandas = df.select(["gold", "dictionary score", "ParlaSent", "GPT"]).to_pandas()
g = sns.PairGrid(
    df_pandas,
    # corner=True,
)
g.map_lower(
    sns.scatterplot,
    size=0.2,
    alpha=0.1,
    color="k",
)
# g.map_lower(corrfunc)
g.map_upper(sns.kdeplot, color="k", levels=5)
# g.map_upper(corrfunc)
g.map_diag(
    sns.histplot,
    color="k",
)
plt.gcf().suptitle(dataset)
plt.tight_layout()
plt.savefig(outpng)
2 + 2
