from pathlib import Path
import json
import re
import polars as pl

try:
    infile = snakemake.input[0]
    outfile = snakemake.output[0]
    lexicoder_path = snakemake.params.lexicoder
    lexicoder_preprocessor_path = snakemake.params.preprocessor
except NameError:
    infile = "data/input/1_coding_a_2010.csv"
    outfile = "data/lsd/1_coding_a_2010.jsonl"
    lexicoder_path = Path("lexicoder_dict", "lexicoder_dict_en.jsonl")
    lexicoder_preprocessor_path = Path("lexicoder_dict", "LSDpreprocess2015.txt")

preprocess = pl.read_csv(
    Path(lexicoder_preprocessor_path),
    separator="\t",
    ignore_errors=True,
    truncate_ragged_lines=True,
    quote_char="<",
)


def lsd(text: str) -> dict[str, int]:
    d = json.loads(Path(lexicoder_path).read_text())
    # preprocess = (
    #     pl.read_csv(
    #         Path(lexicoder_preprocessor_path),
    #         separator="\t",
    #         ignore_errors=True,
    #         truncate_ragged_lines=True,
    #         quote_char="<",
    #     )
    #     .filter(~pl.col("replace").str.contains(r"\["))
    #     .filter(pl.col("module") != "1-punc")
    # )
    # old_text = text
    # for row in preprocess.iter_rows(named=True):
    #     pattern = row["replace"]
    #     pattern = r"\b" + pattern.replace("*", r"[^\s]*") + r"\b"
    #     try:
    #         text = re.sub(pattern=pattern, string=text, repl=row["replace with"])
    #     except re.PatternError:
    #         text = text.replace(row["replace"], row["replace with"])
    #     except TypeError:
    #         continue
    # if text != old_text:
    #     print(f"Old vs new:\n{old_text}\n{text}")
    rdict = dict()
    text = " " + text.casefold() + " "
    for what in ["positive", "negative"]:
        seeds = d[what]
        hitcount = 0
        for seed in seeds:
            pattern = seed.replace("**", "*")
            pattern = pattern.replace("*", r"[^\s]*")
            hits = re.findall(pattern=pattern, string=text)
            if hits:
                # print("seed", seed, "category", what)
                # print(hits)
                text = re.sub(pattern=pattern, string=text, repl=what.upper())
            hitcount += len(hits)
            rdict[f"{what}_words"] = rdict.get(f"{what}_words", []) + hits
            rdict[f"{what}_seeds"] = rdict.get(f"{what}_seeds", []) + [
                seed for i in hits
            ]

        rdict[what] = hitcount
    # print(text)
    return {
        i: rdict[i]
        for i in "positive negative positive_words positive_seeds negative_words negative_seeds".split()
    }


lsd("bog bogged bullied carps")

df = pl.read_csv(infile).with_columns(
    pl.col("Text")
    .map_elements(
        lsd,
        return_dtype=pl.Struct(
            [
                pl.Field("positive", pl.Int64),
                pl.Field("negative", pl.Int64),
                pl.Field("positive_words", pl.List(pl.String)),
                pl.Field("positive_seeds", pl.List(pl.String)),
                pl.Field("negative_words", pl.List(pl.String)),
                pl.Field("negative_seeds", pl.List(pl.String)),
            ]
        ),
    )
    .alias("LSD")
)
df.write_ndjson(outfile)
2 + 2
