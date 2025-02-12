from pathlib import Path

try:
    input_lsd = snakemake.input.lsd
    input_parlasent = snakemake.input.parlasent
    outpng = snakemake.output.png
    outjson = snakemake.output.json
except:
    input_lsd = list(Path("data/lsd/").glob("*.jsonl"))
    input_parlasent = list(Path("data/parlasent/").glob("*.jsonl"))
    outpng = "brisi.png"
    outjson = "brisi.json"

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
    ],
    how="vertical",
)

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
print(df)
df.write_ndjson(outjson)
2 + 2
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# df = df.with_columns(
#     (pl.col("Coding") + np.random.rand(df.shape[0]) * 0.2 - 0.1).alias("Coding")
# )


def corrfunc(x, y, hue=None, ax=None, **kws):
    """Plot the correlation coefficient in the top left hand corner of a plot."""
    r, _ = spearmanr(x, y)
    ax = ax or plt.gca()
    ax.annotate(rf"$\rho$ = {r:.2f}", xy=(0.7, 0.1), xycoords=ax.transAxes)


df_pandas = df.select(
    ["Coding", "ParlaSent", "NetTone", "ExpressedSentiment"]
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
