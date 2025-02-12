import json
from pathlib import Path
import re


f = Path("lexicoder_dict", "lexicoder_dict_en.jsonl")

d = json.loads(f.read_text())


text = "Let's abandon the demonic delusion of accidentally accosting abrasive commoners complicit in conceited contests, contesting abandoning cool relations with daft cynics. Daft, daft daft"
text_ll = " " + text.casefold() + " "

# Negatives:
ns = d["neg_negative"]
for n in ns:
    n = n.replace("**", "*")
    n = r"\b" + n.replace("*", r"[^\s]*")
    hits = re.findall(pattern=n, string=text_ll)
    if hits:
        print(n, hits)
        # break
2 + 2
(num_positive - num_negative) / num_words
