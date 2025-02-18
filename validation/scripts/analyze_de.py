from pathlib import Path

try:
    infile = snakemake.input.parlasent_de
    outpng = snakemake.output.png
    outjson = snakemake.output.json
except:
    infile = "data/parlasent/bundestag_raw_and_counts_DE.jsonl"
    outpng = "brisi.png"
    outjson = "brisi.json"

import polars as pl
import numpy as np

first = pl.read_csv("de_dict/DE_bundestag/bundestag_raw_and_counts_DE.csv")
second = pl.read_csv("de_dict/DE_bundestag/bundestag_sentiment_coding_DE.csv")
third = pl.read_ndjson(infile).select(["ParlaSent", "Qnum"])
df = first.join(second, on="Qnum").join(third, on="Qnum")
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
    pl.col("vote").map_elements(lambda s: mapper.get(s, 99), return_dtype=pl.UInt8)
)


def corrfunc(x, y, hue=None, ax=None, **kws):
    """Plot the correlation coefficient in the top left hand corner of a plot."""
    r, p = spearmanr(x, y)

    ax = ax or plt.gca()
    ax.annotate(rf"$\rho$ = {r:.3f}, {p=:.1e}", xy=(0.1, 0.05), xycoords=ax.transAxes)


df = df.with_columns(pl.col("sentence").str.len_chars().alias("Char Length"))
df_pandas = df.select(
    ["vote", "Char Length", "ParlaSent", "sentiment.norm"]
).to_pandas()
g = sns.PairGrid(
    df_pandas,
)
g.map_lower(
    sns.scatterplot,
    size=0.2,
    alpha=0.1,
    color="k",
)
g.map_lower(corrfunc)
g.map_upper(sns.kdeplot, color="k", levels=5)
g.map_upper(corrfunc)
g.map_diag(
    sns.histplot,
    color="k",
)
plt.tight_layout()
plt.savefig(outpng)
2 + 2
