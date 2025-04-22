from pathlib import Path

try:
    input_lsd = snakemake.input.lsd_coding
    input_parlasent = snakemake.input.parlasent_coding
    input_gpt = snakemake.input.gpt
    outpng = snakemake.output.png
    outjson = snakemake.output.json
    dataset = snakemake.params.name
except NameError as e:
    input_lsd = list(Path("data/lsd/").glob("*coding*.jsonl"))
    input_parlasent = list(Path("data/parlasent/").glob("*coding*.jsonl"))
    input_gpt = "data/english_with_GPT_preds.jsonl"
    outpng = "brisi.png"
    outjson = "brisi.json"
    dataset = "English validation dataset"

import polars as pl
import numpy as np

lsd = pl.concat(
    [
        pl.read_ndjson(i).with_columns(
            pl.lit(Path(i).with_suffix("").name).alias("File")
        )
        for i in input_lsd
    ],
    how="vertical",
)

parlasent = pl.concat(
    [
        pl.read_ndjson(i).with_columns(
            pl.lit(Path(i).with_suffix("").name).alias("File")
        )
        for i in input_parlasent
        if "coding" in str(i)
    ],
    how="vertical_relaxed",
)
gpt = pl.read_ndjson(input_gpt)
df = (
    lsd.select(["Number", "Text", "File", "Coding", "LSD"])
    .join(
        parlasent.select(["Number", "Text", "File", "ParlaSent"]),
        on=["Number", "Text", "File"],
    )
    .with_columns(pl.col("Text").str.split(" ").list.len().alias("Len"))
    .with_columns(
        (
            100
            * (pl.col("LSD").struct["positive"] - pl.col("LSD").struct["negative"])
            / pl.col("Len")
        ).alias("NetTone"),
        (
            (pl.col("LSD").struct["positive"] + 0.5)
            / (pl.col("LSD").struct["negative"] + 0.5)
        )
        .log()
        .alias("ExpressedSentiment"),
    )
    .filter(pl.col("Coding") != 99)
)
df = df.join(
    gpt.select(["text", "GPT_pred"]).unique().rename({"text": "Text"}),
    on="Text",
)
print(df)
df = df.rename(
    {
        "Coding": "gold",
        "GPT_pred": "GPT",
        "NetTone": "dictionary score",
    }
)
df.write_ndjson(outjson)
print("wrote", outjson)
2 + 2
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr


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

2 + 2
